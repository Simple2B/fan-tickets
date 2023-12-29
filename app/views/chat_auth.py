from datetime import datetime
import os
from urllib.parse import urlparse

from sqlalchemy.exc import IntegrityError

from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_user
from flask_mail import Message

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
        template = "chat/chat_auth.html"

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


@chat_auth_blueprint.route("/create_user_email")
def create_user_email():
    try:
        params = s.ChatAuthEmailParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.room_unique_id:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if params.from_sign_up:
        c.save_message("You do not log in. Please log in or sign up", "Sign up", room)
        log(log.INFO, "Sign up from selling")
        return render_template(
            "chat/registration/email.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No email: [%s]", params.user_message)
        return render_template(
            "chat/registration/email.html",
            error_message="Field is empty",
            room=room,
            now=c.utcnow_chat_format(),
        )

    response, user = c.create_email(params.user_message, room)

    if response.is_error:
        return render_template(
            "chat/registration/email.html",
            error_message=response.message,
            room=room,
            now=c.utcnow_chat_format(),
            email_input=response.email,
        )

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_message)
        return render_template(
            "chat/registration/email.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
        )

    try:
        db.session.commit()
        log(log.INFO, f"User {user.email} created")
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User is not created: [%s]", e)
        return render_template(
            "chat/registration/email.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    msg = Message(
        subject=f"Verify email for {CFG.APP_NAME}",
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email],
    )
    msg.html = render_template(
        "email/email_confirm.htm",
        verification_code=response.verification_code,
    )
    mail.send(msg)

    return render_template(
        "chat/registration/email_confirm.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/email_verification")
def email_verification():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()

    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No verification code: [%s]", params.user_message)
        return render_template(
            "chat/registration/email_confirm.html",
            error_message="No verification code, please confirm your email",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            form=form,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if user.verification_code != params.user_message:
        log(log.ERROR, "Wrong verification code: [%s]", params.user_message)
        return render_template(
            "chat/registration/email.confirm.html",
            error_message="Wrong verification code, please confirm your email",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            form=form,
        )

    c.save_message("Please confirm your email", "Email confirmed", room)

    return render_template(
        "chat/registration/password.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.unique_id,
        form=form,
    )


@chat_auth_blueprint.route("/create_user_password", methods=["POST"])
def create_user_password():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error: [%s]",
            form.errors,
        )
        return render_template(
            "chat/registration/password.html",
            error_message="You did not add your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    success = c.create_password(form, room)

    try:
        db.session.commit()
        log(log.INFO, "User password added")
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User is not created: [%s]", e)
        return render_template(
            "chat/registration/password.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not success:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/password.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    return render_template(
        "chat/registration/password_confirm.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=form.user_unique_id.data,
        form=form,
    )


@chat_auth_blueprint.route("/confirm_user_password", methods=["POST"])
def confirm_user_password():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()
    form_file = f.ChatAuthIdentityForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error: [%s]",
            form.errors,
        )
        return render_template(
            "chat/registration/password_confirm.html",
            error_message="Please, confirm your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    success = c.confirm_password(form, room)

    if not success:
        log(log.ERROR, "Password not confirmed: [%s]", form.password.data)
        return render_template(
            "chat/registration/password_confirm.html",
            error_message="Password does not match. Please, confirm your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    return render_template(
        "chat/registration/passport.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=form.user_unique_id.data,
        form=form_file,
    )


@chat_auth_blueprint.route("/create_user_passport", methods=["GET", "POST"])
def create_user_passport():
    form: f.ChatAuthIdentityForm = f.ChatAuthIdentityForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        log(log.ERROR, "Room not found: [%s]", form.room_unique_id.data)
        return render_template(
            "chat/sell/passport.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error, user_unique_id: [%s], room_unique_id: [%s]",
            form.user_unique_id.data,
            form.room_unique_id.data,
        )
        return render_template(
            "chat/registration/passport.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    if not form.file.data:
        log(log.ERROR, "No identification document: [%s]", form.file.data)
        return render_template(
            "chat/registration/passport.html",
            error_message="No verification document, please upload your identification document",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    error_message = c.add_identity_document(form, room)

    if error_message:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/passport.html",
            error_message=error_message,
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    return render_template(
        "chat/registration/name.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=form.user_unique_id.data,
        form=form,
    )


@chat_auth_blueprint.route("/create_user_name")
def create_user_name():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No name provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/name.html",
            error_message="Please, add your name",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    c.create_user_name(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "User name added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User name is not added: [%s]", e)
        return render_template(
            "chat/registration/name.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/registration/last_name.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/create_user_last_name")
def create_user_last_name():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No last name provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/last_name.html",
            error_message="Please, add your last name",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    c.create_user_last_name(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "User last name added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User last name is not added: [%s]", e)
        return render_template(
            "chat/registration/last_name.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/registration/phone.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/create_user_phone")
def create_user_phone():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No last name provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/phone.html",
            error_message="Please, add your phone",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    error_message = c.create_phone(params.user_message, user, room)

    if error_message:
        log(log.ERROR, error_message)
        return render_template(
            "chat/registration/phone.html",
            error_message=error_message,
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            phone=params.user_message,
        )

    try:
        db.session.commit()
        log(log.INFO, "Phone added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Phone is not added: [%s]", e)
        return render_template(
            "chat/registration/phone.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    # parse url and get the domain name
    # TODO: add production url
    if os.environ.get("APP_ENV") == "development":
        parsed_url = urlparse(request.base_url)
        profile_url = f"{parsed_url.scheme}://{parsed_url.netloc}/user/profile"
    else:
        base_url = app.config["STAGING_BASE_URL"]
        profile_url = f"{base_url}user/profile"

    return render_template(
        "chat/registration/address.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.unique_id,
        profile_url=profile_url,
    )


@chat_auth_blueprint.route("/create_user_address")
def create_user_address():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )
    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No address provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/address.html",
            error_message="Please, add your address",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    c.create_address(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "Address added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Address is not added: [%s]", e)
        return render_template(
            "chat/registration/address.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/registration/ask_social_profile.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/create_user_birth_date")
def create_user_birth_date():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No birth date provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/birth_date.html",
            error_message="Please, add your birth date",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    c.create_birth_date(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "Birth date added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Birth date is not added: [%s]", e)
        return render_template(
            "chat/registration/birth_date.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/registration/ask_social_profile.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.unique_id,
    )


@chat_auth_blueprint.route("/create_user_social_profile", methods=["GET", "POST"])
def create_user_social_profile():
    try:
        params = s.ChatAuthSocialProfileParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if params.without_social_profile:
        login_user(user)
        c.save_message("You have successfully registered", "Without social profile", room)

        log(log.INFO, f"User: {user.email} logged in")
        return render_template(
            "chat/registration/verified.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.facebook:
        c.create_social_profile(params, user, room)
        try:
            db.session.commit()
            log(log.INFO, "Facebook added: [%s]", params.user_message)
            return render_template(
                "chat/registration/profile_instagram.html",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )
        except IntegrityError as e:
            db.session.rollback()
            log(log.ERROR, "Facebook is not added: [%s]", e)
            return render_template(
                "chat/registration/profile_facebook.html",
                error_message="Form submitting error. Please add your facebook url again",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )

    if params.without_facebook:
        c.save_message("Do you want to add your facebook profile?", "Without facebook profile", room)
        log(log.INFO, "Without facebook")
        return render_template(
            "chat/registration/profile_instagram.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    if params.instagram:
        c.create_social_profile(params, user, room)
        try:
            db.session.commit()
            log(log.INFO, "Instagram added: [%s]", params.user_message)
            return render_template(
                "chat/registration/profile_twitter.html",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )
        except IntegrityError as e:
            db.session.rollback()
            log(log.ERROR, "Instagram is not added: [%s]", e)
            return render_template(
                "chat/registration/profile_instagram.html",
                error_message="Form submitting error. Please add your instagram url again",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )

    if params.without_instagram:
        c.save_message("Do you want to add your instagram profile?", "Without instagram profile", room)
        log(log.INFO, "Without instagram")
        return render_template(
            "chat/registration/profile_twitter.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    if params.twitter:
        c.create_social_profile(params, user, room)
        try:
            db.session.commit()
            log(log.INFO, "Twitter added: [%s]", params.user_message)

            login_user(user)
            m.Message(
                sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
                room_id=room.id,
                text="You have successfully registered",
            ).save()
            log(log.INFO, f"User: {user.email} logged in")
            return render_template(
                "chat/registration/verified.html",
                room=room,
                now=c.utcnow_chat_format(),
            )
        except IntegrityError as e:
            db.session.rollback()
            log(log.ERROR, "Twitter is not added: [%s]", e)
            return render_template(
                "chat/registration/profile_twitter.html",
                error_message="Form submitting error. Please add your twitter url again",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )

    if params.without_twitter:
        c.save_message("Do you want to add your twitter profile?", "Without twitter profile", room)
        log(log.INFO, "Without twitter")
        login_user(user)
        m.Message(
            sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
            room_id=room.id,
            text="You have successfully registered",
        ).save()
        log(log.INFO, f"User: {user.email} logged in")
        return render_template(
            "chat/registration/verified.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.facebook and not params.instagram and not params.twitter:
        log(log.ERROR, "No social profiles: [%s]", params.facebook)
        return render_template(
            "chat/registration/profile_facebook.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.unique_id,
        )

    return render_template(
        "chat/registration/verified.html",
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_auth_blueprint.route("/home")
def home():
    return render_template("chat/chat_home.html")
