from datetime import datetime
import re
from urllib.parse import urlparse
from flask import request, Blueprint, render_template, flash, current_app as app
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
        buyer_id=2,
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
        flash("Form submitting error", "danger")
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
        )

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found")
        flash("Room not found", "danger")
        return render_template(
            "chat/chat_error.html",
            error_message="Room not found",
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
    user = m.User(
        username=user_name,
        email=app.config["CHAT_DEFAULT_EMAIL"],
        phone=app.config["CHAT_DEFAULT_PHONE"],
        card=app.config["CHAT_DEFAULT_CARD"],
        password="",
    ).save(False)
    db.session.flush()
    room.seller_id = user.id
    db.session.commit()
    log(log.INFO, f"User {user_name} created")
    flash(f"User {user_name} created", "success")

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
    email = request.args.get("chat_email")
    user_unique_id = request.args.get("user_unique_id")

    if not email or not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error")
        flash("Form submitting error", "danger")
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
        )

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your email",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=email,
    ).save(False)
    user.email = str(email)  # mypy made me do it!
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
    phone = request.args.get("chat_phone")
    user_unique_id = request.args.get("user_unique_id")

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room_unique_id or not user_unique_id:
        log(log.ERROR, "Form submitting error")
        flash("Form submitting error", "danger")
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
        )

    pattern = r"^\+?\d{10,13}$"
    match_pattern = re.search(pattern, str(phone))

    if not phone or not match_pattern:
        return render_template(
            "chat/chat_04_phone.html",
            now=now_str,
            room=room,
            user=user,
        )

    # parse url and get the domain name
    parsed_url = urlparse(request.base_url)
    profile_url = f"{parsed_url.scheme}://{parsed_url.netloc}/user/profile"

    success_message = "Você foi registrado com sucesso. Por favor, verifique seu perfil."

    login_user(user, remember=True)

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please input your phone",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=phone,
    ).save(False)
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=success_message,
    ).save(False)
    user.phone = str(phone)  # mypy made me do it!
    db.session.commit()

    return render_template(
        "chat/chat_05_verified.html",
        now=now_str,
        room=room,
        user=user,
        profile_url=profile_url,
    )
