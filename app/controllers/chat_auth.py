from datetime import datetime
from random import randint
import re

from flask import render_template, current_app as app
from flask_mail import Message

from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db, mail

from app.logger import log
from config import config

CFG = config()


def check_user_room_id(params: s.ChatAuthParams) -> tuple[s.ChatAuthResultParams, m.User | None, m.Room | None]:
    """
    The function to check and validate params.

    At the moment it returns response with template for chat if params are not valid or
    return params, room, user, datetime as string if params are valid.
    """
    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == params.room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    # TODO: is needed to create a room if it does not exist?
    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return s.ChatAuthResultParams(now_str=now_str, params=params, is_error=True), None, room

    if not params.room_unique_id or not params.user_unique_id:
        log(
            log.ERROR,
            "Form submitting error, user_unique_id: [%s], room_unique_id: [%s]",
            params.user_unique_id,
            params.room_unique_id,
        )
        return s.ChatAuthResultParams(now_str=now_str, params=params, is_error=True), None, room

    user_query = m.User.select().where(m.User.unique_id == params.user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return s.ChatAuthResultParams(now_str=now_str, params=params, is_error=True), user, room

    return s.ChatAuthResultParams(now_str=now_str, params=params, user=user), user, room


def send_message(bot_message: str, user_message: str, room: m.Room):
    """
    The function to save message for history in chat.
    It is save message from chat-bot and user.
    """
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=bot_message,
    ).save(False)
    m.Message(
        room_id=room.id,
        text=user_message,
    ).save()

    log(log.INFO, "Messages for history saved. Bot: [%s], user: [%s]", bot_message, user_message)


def create_email(email: str, room: m.Room) -> tuple[s.ChatAuthEmailValidate, m.User | None]:
    pattern = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    match_pattern = re.search(pattern, email.lower())

    if not match_pattern:
        return s.ChatAuthEmailValidate(email=email, message="Invalid email format", is_error=True), None

    user_email_query = m.User.select().where(m.User.email == email)
    user_email: m.User = db.session.scalar(user_email_query)

    if user_email:
        return s.ChatAuthEmailValidate(email=email, message="Email already taken", is_error=True), None

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
        email=email,
        phone=app.config["CHAT_DEFAULT_PHONE"],
        card=app.config["CHAT_DEFAULT_CARD"],
        password="",
        verification_code=verification_code,
    ).save(False)

    msg = Message(
        subject=f"Verify email for {CFG.APP_NAME}",
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email],
    )
    msg.html = render_template(
        "email/email_confirm.htm",
        verification_code=verification_code,
    )
    mail.send(msg)

    db.session.flush()
    room.seller_id = user.id
    db.session.commit()
    log(log.INFO, f"User {email} created")

    send_message("Please input your email", f"Email: {email}", room)

    return s.ChatAuthEmailValidate(email=email), user


def create_password(form: f.ChatAuthPasswordForm, room: m.Room) -> bool:
    user_query = m.User.select().where(m.User.unique_id == form.user_unique_id.data)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return False

    user.password = form.password.data
    user.save()

    send_message("Please input your password", "Password has been created", room)

    return True


def add_identity_document(form: f.ChatAuthIdentityForm, room: m.Room) -> str:
    user_query = m.User.select().where(m.User.unique_id == form.user_unique_id.data)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return "Form submitting error"

    response = c.image_upload(user, c.type_image.IDENTIFICATION)

    if 200 not in response:
        return "Not valid type of verification document, please upload your identification document with right format"

    send_message("Please upload your identification document", "Identification document has been uploaded", room)

    return ""


def create_user_name(params: s.ChatAuthParams, user: m.User, room: m.Room):
    user.name = params.name
    user.save()

    send_message("Please input your name", f"Name: {params.name}", room)


def create_user_last_name(params: s.ChatAuthParams, user: m.User, room: m.Room):
    user.last_name = params.last_name
    user.save()

    send_message("Please input your last name", f"Last name: {params.last_name}", room)


def create_phone(phone: str, user: m.User, room: m.Room) -> str:
    pattern = r"^\+?\d{10,13}$"
    match_pattern = re.search(pattern, str(phone))

    if not match_pattern:
        return "Invalid phone format"

    user_phone_query = m.User.select().where(m.User.phone == phone)
    user_phone: m.User = db.session.scalar(user_phone_query)

    if user_phone:
        return "Phone already taken"

    user.phone = phone
    user.save()

    send_message("Please input your phone", f"Phone: {phone}", room)

    return ""


def create_address(address: str, user: m.User, room: m.Room):
    user.address = address
    user.activated = True
    user.save()

    send_message("Please input your address", f"Address: {address}", room)


def create_social_profiles(params: s.ChatAuthParams, user: m.User, room: m.Room):
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
    ).save()
