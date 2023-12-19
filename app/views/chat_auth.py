from datetime import datetime
from random import randint
import re
import os
from urllib.parse import urlparse
from flask import request, Blueprint, render_template, current_app as app
from flask_mail import Message
from flask_login import current_user, login_user
from app.controllers import image_upload, type_image, check_user_room_id, send_message
from app import schema as s
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

    pattern = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    match_pattern = re.search(pattern, (params.email).lower())
    if not match_pattern:
        return render_template(
            "chat/registration/01_email.html",
            error_message="Invalid email format",
            room=room,
            now=now_str,
            email_input=params.email,
        )

    email_query = m.User.select().where(m.User.email == params.email)
    email: m.User = db.session.scalar(email_query)

    if email:
        log(log.ERROR, "Email already taken")
        return render_template(
            "chat/registration/01_email.html",
            error_message="Email already taken",
            room=room,
            now=now_str,
            email_input=params.email,
        )

    picture_query = m.Picture.select().where(m.Picture.filename.ilike(f"%{'default_avatar'}%"))
    picture: m.Picture = db.session.scalar(picture_query)
    identity_document_query = m.Picture.select().where(m.Picture.filename.ilike(f"%{'default_passport'}%"))
    identity_document = db.session.scalar(identity_document_query)
    picture_id = picture.id if picture else None
    identity_document_id = identity_document.id if identity_document else None
    verification_code = randint(100000, 999999)
    user = m.User(
        # Since in chat registration we get user's info step by step,
        # asking user to input credentials one by one,
        # we need to fill the rest of the fields with default values
        picture_id=picture_id,
        identity_document_id=identity_document_id,
        email=params.email,
        phone=app.config["CHAT_DEFAULT_PHONE"],
        card=app.config["CHAT_DEFAULT_CARD"],
        password="",
        verification_code=verification_code,
    ).save(False)

    msg = Message(
        subject=f"Verify email for {CFG.APP_NAME}",
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[params.email],
    )
    msg.html = render_template(
        "email/email_confirm.htm",
        verification_code=verification_code,
    )
    mail.send(msg)

    db.session.flush()
    room.seller_id = user.id
    db.session.commit()
    log(log.INFO, f"User {params.email} created")

    send_message("Please input your email", f"Email: {params.email}", room)

    user.email = str(params.email)  # mypy made me do it!
    db.session.commit()

    return render_template(
        "chat/registration/02_confirm_email.html",
        now=now_str,
        room=room,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/email_verification")
def email_verification():
    params, user, room, now_str = check_user_room_id("chat/registration/02_confirm_email.html")

    if not params or not user or not room or not now_str:
        log(
            log.ERROR, "check_user_room_id not return correct data: [%s], [%s], [%s], [%s]", params, user, room, now_str
        )
        return render_template(
            "chat/registration/02_confirm_email.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    if not params.verification_code:
        log(log.ERROR, "No verification code: [%s]", params.verification_code)
        return render_template(
            "chat/registration/02_confirm_email.html",
            error_message="No verification code, please confirm your email",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    if user.verification_code != params.verification_code:
        log(log.ERROR, "Wrong verification code: [%s]", params.verification_code)
        return render_template(
            "chat/registration/02_confirm_email.html",
            error_message="Wrong verification code, please confirm your email",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    send_message("Please confirm your email", "Email confirmed", room)
    db.session.commit()

    return render_template(
        "chat/registration/03_pass.html",
        now=now_str,
        room=room,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/password", methods=["GET", "POST"])
def password():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    user_unique_id = request.args.get("user_unique_id")
    password = request.args.get("chat_password")
    confirm_password = request.args.get("chat_confirm_password")

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not password or not confirm_password:
        log(log.ERROR, "Form submitting error")
        return render_template(
            "chat/registration/03_pass.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if password != confirm_password:
        return render_template(
            "chat/registration/03_pass.html",
            now=now_str,
            room=room,
            user_unique_id=user_unique_id,
            error="Passwords don't match",
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your password",
    ).save(False)
    m.Message(
        room_id=room.id,
        text="Password has been created",
    ).save(False)
    user.password = password
    db.session.commit()

    return render_template(
        "chat/registration/04_identification.html",
        now=now_str,
        room=room,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/identification", methods=["GET", "POST"])
def identification():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.form.get("room_unique_id")
    user_unique_id = request.form.get("user_unique_id")
    document_input = request.files.get("file")

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error, user: [%s], room: [%s]", user_unique_id, room_unique_id)
        return render_template(
            "chat/registration/04_identification.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/04_identification.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not document_input:
        log(log.ERROR, "No identification document: [%s]", document_input)
        return render_template(
            "chat/registration/04_identification.html",
            error_message="No verification document, please upload your identification document",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", user_unique_id)
        return render_template(
            "chat/registration/04_identification.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    # TODO: change to more detailed validation
    response = image_upload(user, type_image.IDENTIFICATION)

    if 200 not in response:
        log(log.ERROR, "Not valid identification document: [%s]", document_input)
        return render_template(
            "chat/registration/04_identification.html",
            error_message="Not valid type of verification document, please upload your identification document with right format",
            room=room,
            now=now_str,
            user_unique_id=user.unique_id,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please upload your identification document",
    ).save(False)
    m.Message(
        room_id=room.id,
        text="Identification document has been uploaded",
    ).save(False)

    db.session.commit()

    return render_template(
        "chat/registration/05_name.html",
        room=room,
        now=now_str,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/create_name", methods=["GET", "POST"])
def create_name():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    user_unique_id = request.args.get("user_unique_id")
    name_input = request.args.get("chat_name")

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error, user: [%s], room: [%s]", user_unique_id, room_unique_id)
        return render_template(
            "chat/registration/05_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/registration/05_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not name_input:
        log(log.ERROR, "No name_input: [%s]", name_input)
        return render_template(
            "chat/registration/05_name.html",
            error_message="Please, add your name",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", user_unique_id)
        return render_template(
            "chat/registration/05_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    user.name = name_input
    user.save(False)

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your name",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=f"Name: {name_input}",
    ).save(False)
    db.session.commit()

    return render_template(
        "chat/registration/06_last_name.html",
        room=room,
        now=now_str,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/create_last_name", methods=["GET", "POST"])
def create_last_name():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    user_unique_id = request.args.get("user_unique_id")
    last_name_input = request.args.get("chat_last_name")

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error, user: [%s], room: [%s]", user_unique_id, room_unique_id)
        return render_template(
            "chat/registration/06_last_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/06_last_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not last_name_input:
        log(log.ERROR, "No name_input: [%s]", last_name_input)
        return render_template(
            "chat/registration/06_last_name.html",
            error_message="Please, add your last name",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", user_unique_id)
        return render_template(
            "chat/registration/06_last_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    user.last_name = last_name_input
    user.save(False)

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your last name",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=f"Last name: {last_name_input}",
    ).save(False)
    db.session.commit()

    return render_template(
        "chat/registration/07_phone.html",
        room=room,
        now=now_str,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/phone", methods=["GET", "POST"])
def phone():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    phone_input = request.args.get("chat_phone")
    user_unique_id = request.args.get("user_unique_id")

    if not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error")
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
        )

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    pattern = r"^\+?\d{10,13}$"
    match_pattern = re.search(pattern, str(phone_input))

    if not phone_input or not match_pattern:
        return render_template(
            "chat/registration/07_phone.html",
            error_message="Invalid phone format",
            now=now_str,
            room=room,
            user_unique_id=user_unique_id,
        )

    phone_query = m.User.select().where(m.User.phone == phone_input)
    phone: m.User = db.session.scalar(phone_query)

    if phone:
        log(log.ERROR, "Phone already taken")
        return render_template(
            "chat/registration/07_phone.html",
            error_message="Phone already taken",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
            phone_input=phone_input,
        )

    # parse url and get the domain name

    # TODO: add production url
    if os.environ.get("APP_ENV") == "development":
        parsed_url = urlparse(request.base_url)
        profile_url = f"{parsed_url.scheme}://{parsed_url.netloc}/user/profile"
    else:
        base_url = app.config["STAGING_BASE_URL"]
        profile_url = f"{base_url}user/profile"

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your phone",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=f"Phone: {phone_input}",
    ).save(False)
    user.phone = str(phone_input)  # mypy made me do it!
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
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    user_unique_id = request.args.get("user_unique_id")
    address_input = request.args.get("address")

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error, user: [%s], room: [%s]", user_unique_id, room_unique_id)
        return render_template(
            "chat/registration/08_address.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/08_address.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not address_input:
        log(log.ERROR, "No name_input: [%s]", address_input)
        return render_template(
            "chat/registration/08_address.html",
            error_message="Please, add your address",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", user_unique_id)
        return render_template(
            "chat/registration/08_address.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    user.name = address_input
    user.save(False)

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your address",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=f"Address: {address_input}",
    ).save(False)

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
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    user_unique_id = request.args.get("user_unique_id")
    without_social_profile = request.args.get("without_social_profile")
    facebook_input = request.args.get("facebook")
    instagram_input = request.args.get("instagram")
    twitter_input = request.args.get("twitter")

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error, user: [%s], room: [%s]", user_unique_id, room_unique_id)
        return render_template(
            "chat/registration/09_ask_social_profile.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/09_ask_social_profile.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", user_unique_id)
        return render_template(
            "chat/registration/09_ask_social_profile.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=user_unique_id,
        )

    if without_social_profile:
        login_user(user)
        m.Message(
            sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
            room_id=room.id,
            text="You have been registered successfully",
        ).save(False)
        m.Message(
            room_id=room.id,
            text="Without social profile",
        ).save(False)
        db.session.commit()

        log(log.INFO, f"User {user_unique_id} logged in")
        return render_template(
            "chat/registration/11_verified.html",
            room=room,
            now=now_str,
        )

    if not facebook_input and not instagram_input and not twitter_input:
        log(log.ERROR, "No social profile: [%s]", facebook_input)
        return render_template(
            "chat/registration/10_social_profiles.html",
            room=room,
            now=now_str,
            user_unique_id=user.unique_id,
        )

    message = ""

    if facebook_input:
        user.facebook = facebook_input
        message += f"facebook: {facebook_input}\n"
    if instagram_input:
        user.instagram = instagram_input
        message += f"instagram: {instagram_input}\n"
    if twitter_input:
        user.twitter = twitter_input
        message += f"twitter: {twitter_input}\n"

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please add your social profiles",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=message,
    ).save(False)
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Você foi registrado com sucesso. Por favor, verifique seu perfil.",
    ).save(False)
    db.session.commit()

    login_user(user)
    log(log.INFO, f"User {user_unique_id} logged in")

    return render_template(
        "chat/registration/11_verified.html",
        room=room,
        now=now_str,
    )


@chat_auth_blueprint.route("/home")
def home():
    return render_template("chat/chat_home.html")
