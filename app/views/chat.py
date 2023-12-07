from datetime import datetime
import re
import os
from urllib.parse import urlparse
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_user
from app import models as m, db
from app.logger import log
from config import config

CFG = config()

chat_blueprint = Blueprint("chat", __name__, url_prefix="/chat")


@chat_blueprint.route("/sell", methods=["GET", "POST"])
def sell():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    question = "Are you looking for buying or selling tickets or for events information?"

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

    return render_template(
        "chat/chat_01_username.html",
        now=now_str,
        room=room,
    )


@chat_blueprint.route("/username", methods=["GET", "POST"])
def username():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    user_name = request.args.get("chat_username")

    if not user_name or not room_unique_id:
        log(log.ERROR, "Form submitting error")
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
        )

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found")
        return render_template(
            "chat/chat_error.html",
            error_message="Room not found",
        )

    user_query = m.User.select().where(m.User.username == user_name)
    user: m.User = db.session.scalar(user_query)

    if user:
        log(log.ERROR, "User already exists")
        return render_template(
            "chat/chat_01_username.html",
            error_message="User already exists",
            room=room,
            now=now_str,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Then let's get started!",
    ).save(False)
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your username",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=user_name,
    ).save(False)

    picture_query = m.Picture.select().where(m.Picture.filename.ilike(f"%{'default_avatar'}%"))
    picture: m.Picture = db.session.scalar(picture_query)
    picture_id = picture.id if picture else None
    user = m.User(
        # Since in chat registration we get user's info step by step,
        # asking user to input credentials one by one,
        # we need to fill the rest of the fields with default values
        username=user_name,
        picture_id=picture_id,
        email=app.config["CHAT_DEFAULT_EMAIL"],
        phone=app.config["CHAT_DEFAULT_PHONE"],
        card=app.config["CHAT_DEFAULT_CARD"],
        password="",
    ).save(False)
    db.session.flush()
    room.seller_id = user.id
    db.session.commit()
    log(log.INFO, f"User {user_name} created")

    return render_template(
        "chat/chat_02_email.html",
        now=now_str,
        room=room,
        user=user,
    )


@chat_blueprint.route("/email", methods=["GET", "POST"])
def email():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    email_input = request.args.get("chat_email")
    user_unique_id = request.args.get("user_unique_id")

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not email_input or not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error")
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=user,
            email_input=email_input,
        )

    pattern = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    match_pattern = re.search(pattern, email_input)
    if not match_pattern:
        return render_template(
            "chat/chat_02_email.html",
            error_message="Invalid email format",
            room=room,
            now=now_str,
            user=user,
            email_input=email_input,
        )

    email_query = m.User.select().where(m.User.email == email_input)
    email: m.User = db.session.scalar(email_query)

    if email:
        log(log.ERROR, "Email already taken")
        return render_template(
            "chat/chat_02_email.html",
            error_message="Email already taken",
            room=room,
            now=now_str,
            user=user,
            email_input=email_input,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your email",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=email_input,
    ).save(False)
    user.email = str(email_input)  # mypy made me do it!
    db.session.commit()

    return render_template(
        "chat/chat_03_pass.html",
        now=now_str,
        room=room,
        user=user,
    )


@chat_blueprint.route("/password", methods=["GET", "POST"])
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

    if password != confirm_password:
        return render_template(
            "chat/chat_03_pass.html",
            now=now_str,
            room=room,
            user=user,
            error="Passwords don't match",
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your password",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=password,
    ).save(False)
    user.password = password
    db.session.commit()

    return render_template(
        "chat/chat_04_phone.html",
        now=now_str,
        room=room,
        user=user,
    )


@chat_blueprint.route("/phone", methods=["GET", "POST"])
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
            "chat/chat_04_phone.html",
            now=now_str,
            room=room,
            user=user,
        )

    phone_query = m.User.select().where(m.User.phone == phone_input)
    phone: m.User = db.session.scalar(phone_query)

    if phone:
        log(log.ERROR, "Phone already taken")
        return render_template(
            "chat/chat_04_phone.html",
            error_message="Phone already taken",
            room=room,
            now=now_str,
            user=user,
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

    success_message = "Você foi registrado com sucesso. Por favor, verifique seu perfil."

    login_user(user)

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your phone",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=phone_input,
    ).save(False)
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=success_message,
    ).save(False)
    user.phone = str(phone_input)  # mypy made me do it!
    db.session.commit()

    return render_template(
        "chat/chat_05_verified.html",
        now=now_str,
        room=room,
        user=user,
        profile_url=profile_url,
    )
