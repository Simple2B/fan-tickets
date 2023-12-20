from datetime import datetime
from random import randint
import re
import os
from urllib.parse import urlparse
from flask import request, Blueprint, render_template, current_app as app
from flask_mail import Message
from flask_login import current_user, login_user
from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db, mail
from app.logger import log
from config import config

CFG = config()

chat_auth_blueprint = Blueprint("chat", __name__, url_prefix="/chat")


@chat_auth_blueprint.route("/login_form", methods=["GET", "POST"])
def login_form():
    room_unique_id = request.args.get("room_unique_id")
    ticket_unique_id = request.args.get("ticket_unique_id")
    login_from_navbar = request.args.get("login_from_navbar")
    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if login_from_navbar:
        room = m.Room(
            buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
        ).save()

    if not room:
        log(log.ERROR, "Room not found")
        return render_template(
            "chat/registration/00_login_form.html",
            error_message="Room not found",
        )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    return render_template(
        "chat/registration/00_login_form.html",
        room=room,
        ticket=ticket,
    )


@chat_auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    chat_email = request.args.get("chat_email")
    chat_password = request.args.get("chat_password")
    room_unique_id = request.args.get("room_unique_id")
    ticket_unique_id = request.args.get("ticket_unique_id")

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found")
        return render_template(
            "chat/registration/00_login_form.html",
            error_message="Room not found",
        )

    user: m.User = m.User.authenticate(chat_email, chat_password)
    if not user:
        log(log.ERROR, "Wrong email or password")
        return render_template(
            "chat/registration/00_login_form.html",
            error_message="Wrong email or password",
            room=room,
        )

    login_user(user)
    log(log.INFO, "Login successful.")

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    ticket.is_in_cart = True
    ticket.buyer_id = user.id
    ticket.save()

    cart_tickets_query = m.Ticket.select().where(m.Ticket.buyer == current_user)
    cart_tickets = db.session.scalars(cart_tickets_query).all()
    total_price = sum([ticket.price_gross for ticket in cart_tickets])

    return render_template(
        "chat/buy/tickets_06_cart.html",
        room=room,
        cart_tickets=cart_tickets,
        total_price=total_price,
    )


@chat_auth_blueprint.route("/sell", methods=["GET", "POST"])
def sell():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    question = "Are you looking for buying or selling tickets?"

    seller_id = current_user.id if current_user.is_authenticated else None
    room = m.Room(
        seller_id=seller_id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=question,
    ).save(False)
    m.Message(
        sender_id=seller_id,
        room_id=room.id,
        text="Selling",
    ).save(False)
    db.session.commit()

    if current_user.is_authenticated:
        template = "chat/sell/01_event_name.html"
    else:
        template = "chat/registration/01_email.html"

    return render_template(
        template,
        locations=m.Location.all(),
        now=now_str,
        room=room,
        user=current_user,
    )


@chat_auth_blueprint.route("/buy", methods=["GET", "POST"])
def buy():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = m.Room(
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Are you looking for buying or selling tickets?",
    ).save(False)
    m.Message(
        room_id=room.id,
        text="Buying",
    ).save(False)
    db.session.commit()

    return render_template(
        "chat/buy/events_01_filters.html",
        locations=m.Location.all(),
        now=now_str,
        room=room,
    )


@chat_auth_blueprint.route("/email", methods=["GET", "POST"])
def email():
    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    params = s.ChatAuthParams.model_validate(dict(request.args))

    room_query = m.Room.select().where(m.Room.unique_id == params.room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not params.email or not params.room_unique_id:
        log(log.ERROR, "Form submitting error")
        return render_template(
            "chat/registration/01_email.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            email_input=params.email,
        )

    response, user = c.create_email(params.email, room)

    if response.is_error:
        return render_template(
            "chat/registration/01_email.html",
            error_message=response.message,
            room=room,
            now=now_str,
            email_input=response.email,
        )

    assert user

    return render_template(
        "chat/registration/02_confirm_email.html",
        now=now_str,
        room=room,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/email_verification")
def email_verification():
    params = s.ChatAuthParams.model_validate(dict(request.args))
    response, user, room = c.check_user_room_id(params)

    if response.is_error:
        log(
            log.ERROR,
            "check_user_room_id return not correct data params:[%s], user_id:[%s], room_id:[%s], now_str:[%s]",
            response.params,
            user,
            room,
            response.now_str,
        )
        return render_template(
            "chat/registration/05_name.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
            user_unique_id=response.params.user_unique_id,
        )

    if not params.verification_code:
        log(log.ERROR, "No verification code: [%s]", params.verification_code)
        return render_template(
            "chat/registration/02_confirm_email.html",
            error_message="No verification code, please confirm your email",
            room=room,
            now=response.now_str,
            user_unique_id=params.user_unique_id,
        )

    assert user
    assert room

    if user.verification_code != params.verification_code:
        log(log.ERROR, "Wrong verification code: [%s]", params.verification_code)
        return render_template(
            "chat/registration/02_confirm_email.html",
            error_message="Wrong verification code, please confirm your email",
            room=room,
            now=response.now_str,
            user_unique_id=params.user_unique_id,
        )

    c.send_message("Please confirm your email", "Email confirmed", room)

    return render_template(
        "chat/registration/03_pass.html",
        now=response.now_str,
        room=room,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/password", methods=["POST"])
def password():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()

    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == form.room_unique_id.data)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found: [%s]", form.room_unique_id.data)
        return render_template(
            "chat/sell/03_pass.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error, user_unique_id: [%s], room_unique_id: [%s]",
            form.user_unique_id.data,
            form.room_unique_id.data,
        )
        return render_template(
            "chat/registration/03_pass.html",
            error_message="Form submitting error. Please, add your password",
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    if form.password.data != form.confirm_password.data:
        return render_template(
            "chat/registration/03_pass.html",
            now=now_str,
            room=room,
            user_unique_id=form.user_unique_id.data,
            error="Passwords do not match",
        )

    success = c.create_password(form, room)

    if not success:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/03_pass.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    return render_template(
        "chat/registration/04_identification.html",
        now=now_str,
        room=room,
        user_unique_id=form.user_unique_id.data,
    )


@chat_auth_blueprint.route("/identification", methods=["GET", "POST"])
def identification():
    form: f.ChatAuthIdentityForm = f.ChatAuthIdentityForm()

    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == form.room_unique_id.data)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found: [%s]", form.room_unique_id.data)
        return render_template(
            "chat/sell/04_identification.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error, user_unique_id: [%s], room_unique_id: [%s]",
            form.user_unique_id.data,
            form.room_unique_id.data,
        )
        return render_template(
            "chat/registration/04_identification.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    if not form.file.data:
        log(log.ERROR, "No identification document: [%s]", form.file.data)
        return render_template(
            "chat/registration/04_identification.html",
            error_message="No verification document, please upload your identification document",
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    error_message = c.add_identity_document(form, room)

    if error_message:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/04_identification.html",
            error_message=error_message,
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    return render_template(
        "chat/registration/05_name.html",
        room=room,
        now=now_str,
        user_unique_id=form.user_unique_id.data,
    )


@chat_auth_blueprint.route("/create_name")
def create_name():
    data = s.ChatAuthParams.model_validate(dict(request.args))
    response, user, room = c.check_user_room_id(data)

    if response.is_error:
        log(
            log.ERROR,
            "check_user_room_id return not correct data params:[%s], user_id:[%s], room_id:[%s], now_str:[%s]",
            response.params,
            user,
            room,
            response.now_str,
        )
        return render_template(
            "chat/registration/05_name.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
            user_unique_id=response.params.user_unique_id,
        )

    if not response.params.name:
        log(log.ERROR, "Name not found: [%s]", response.params.name)
        return render_template(
            "chat/registration/05_name.html",
            error_message="Please, add your name",
            room=room,
            now=response.now_str,
            user_unique_id=response.params.user_unique_id,
        )

    assert user
    assert room
    c.create_user_name(response.params, user, room)

    return render_template(
        "chat/registration/06_last_name.html",
        room=room,
        now=response.now_str,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/create_last_name", methods=["GET", "POST"])
def create_last_name():
    response = check_user_room_id()
    params: s.ChatAuthParams = response["params"]
    now_str = response["now_str"]
    if response["room"]:
        room: m.Room = response["room"]
    if response["user"]:
        user: m.User = response["user"]

    if response["is_error"]:
        log(
            log.ERROR,
            "check_user_room_id return not correct data params:[%s], user_id:[%s], room_id:[%s], now_str:[%s]",
            params,
            response["user"],
            response["room"],
            now_str,
        )
        return render_template(
            "chat/registration/06_last_name.html",
            error_message="Form submitting error",
            room=response["room"],
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    if not params.last_name:
        log(log.ERROR, "No name_input: [%s]", params.last_name)
        return render_template(
            "chat/registration/06_last_name.html",
            error_message="Please, add your last name",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    user.last_name = params.last_name
    user.save(False)

    send_message("Please input your last name", f"Last name: {params.last_name}", room)

    db.session.commit()

    return render_template(
        "chat/registration/07_phone.html",
        room=room,
        now=now_str,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/phone", methods=["GET", "POST"])
def phone():
    response = check_user_room_id()
    params: s.ChatAuthParams = response["params"]
    now_str = response["now_str"]
    if response["room"]:
        room: m.Room = response["room"]
    if response["user"]:
        user: m.User = response["user"]

    if response["is_error"]:
        log(
            log.ERROR,
            "check_user_room_id return not correct data params:[%s], user_id:[%s], room_id:[%s], now_str:[%s]",
            params,
            response["user"],
            response["room"],
            now_str,
        )
        return render_template(
            "chat/registration/06_last_name.html",
            error_message="Form submitting error",
            room=response["room"],
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    pattern = r"^\+?\d{10,13}$"
    match_pattern = re.search(pattern, str(params.phone))

    if not params.phone or not match_pattern:
        return render_template(
            "chat/registration/07_phone.html",
            error_message="Invalid phone format",
            now=now_str,
            room=room,
            user_unique_id=params.user_unique_id,
        )

    phone_query = m.User.select().where(m.User.phone == params.phone)
    phone: m.User = db.session.scalar(phone_query)

    if phone:
        log(log.ERROR, "Phone already taken")
        return render_template(
            "chat/registration/07_phone.html",
            error_message="Phone already taken",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
            phone=params.phone,
        )

    # parse url and get the domain name
    # TODO: add production url
    if os.environ.get("APP_ENV") == "development":
        parsed_url = urlparse(request.base_url)
        profile_url = f"{parsed_url.scheme}://{parsed_url.netloc}/user/profile"
    else:
        base_url = app.config["STAGING_BASE_URL"]
        profile_url = f"{base_url}user/profile"

    send_message("Please input your phone", f"Phone: {params.phone}", room)

    user.phone = str(params.phone)  # mypy made me do it!
    db.session.commit()

    return render_template(
        "chat/registration/08_address.html",
        now=now_str,
        room=room,
        user_unique_id=user.unique_id,
        profile_url=profile_url,
    )


@chat_auth_blueprint.route("/address", methods=["GET", "POST"])
def address():
    response = check_user_room_id()
    params: s.ChatAuthParams = response["params"]
    now_str = response["now_str"]
    if response["room"]:
        room: m.Room = response["room"]
    if response["user"]:
        user: m.User = response["user"]

    if response["is_error"]:
        log(
            log.ERROR,
            "check_user_room_id return not correct data params:[%s], user_id:[%s], room_id:[%s], now_str:[%s]",
            params,
            response["user"],
            response["room"],
            now_str,
        )
        return render_template(
            "chat/registration/06_last_name.html",
            error_message="Form submitting error",
            room=response["room"],
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    if not params.address:
        log(log.ERROR, "No name_input: [%s]", params.address)
        return render_template(
            "chat/registration/08_address.html",
            error_message="Please, add your address",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    user.name = params.address
    user.save(False)

    send_message("Please input your address", f"Address: {params.address}", room)

    user.activated = True
    db.session.commit()

    return render_template(
        "chat/registration/09_ask_social_profile.html",
        room=room,
        now=now_str,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/social_profile", methods=["GET", "POST"])
def social_profile():
    response = check_user_room_id()
    params: s.ChatAuthParams = response["params"]
    now_str = response["now_str"]
    if response["room"]:
        room: m.Room = response["room"]
    if response["user"]:
        user: m.User = response["user"]

    if response["is_error"]:
        log(
            log.ERROR,
            "check_user_room_id return not correct data params:[%s], user_id:[%s], room_id:[%s], now_str:[%s]",
            params,
            response["user"],
            response["room"],
            now_str,
        )
        return render_template(
            "chat/registration/06_last_name.html",
            error_message="Form submitting error",
            room=response["room"],
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    if params.without_social_profile:
        login_user(user)
        send_message("You have been registered successfully", "Without social profile", room)

        log(log.INFO, f"User: {params.user_unique_id} logged in")
        return render_template(
            "chat/registration/11_verified.html",
            room=room,
            now=now_str,
        )

    if not params.facebook and not params.instagram and not params.twitter:
        log(log.ERROR, "No social profile: [%s]", params.facebook)
        return render_template(
            "chat/registration/10_social_profiles.html",
            room=room,
            now=now_str,
            user_unique_id=user.unique_id,
        )

    message = ""

    if params.facebook:
        user.facebook = params.facebook
        message += f"facebook: {params.facebook}\n"
    if params.instagram:
        user.instagram = params.instagram
        message += f"instagram: {params.instagram}\n"
    if params.twitter:
        user.twitter = params.twitter
        message += f"twitter: {params.twitter}\n"

    send_message("Please add your social profiles", message, room)

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Você foi registrado com sucesso. Por favor, verifique seu perfil.",
    ).save(False)
    db.session.commit()

    login_user(user)
    log(log.INFO, f"User: {params.user_unique_id} logged in")

    return render_template(
        "chat/registration/11_verified.html",
        room=room,
        now=now_str,
    )


@chat_auth_blueprint.route("/home")
def home():
    return render_template("chat/chat_home.html")
