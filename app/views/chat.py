from datetime import datetime
from twilio.rest import Client
from flask import request, Blueprint, render_template, flash, current_app as app
from flask_login import current_user
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
        sender_id=2,
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

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    m.Message(
        sender_id=2,
        room_id=room.id,
        text="Then let's get started!",
    ).save(False)
    m.Message(
        sender_id=2,
        room_id=room.id,
        text="Please input your username",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=user_name,
    ).save(False)
    user = m.User(
        username=user_name,
        email="empty@email.com",
        phone="00000000000",
        card="0000000000000000",
        password="",
    ).save(False)
    db.session.flush()
    room.seller_id = user.id
    db.session.commit()

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

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    m.Message(
        sender_id=2,
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
        sender_id=2,
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

    m.Message(
        sender_id=2,
        room_id=room.id,
        text="Please input your phone",
    ).save(False)
    m.Message(
        room_id=room.id,
        text=phone,
    ).save(False)
    user.phone = str(phone)  # mypy made me do it!
    db.session.commit()

    return render_template(
        "chat/chat_03_pass.html",
        now=now_str,
        room=room,
        user=user,
    )


@chat_blueprint.route("/send-code", methods=["GET", "POST"])
def send_code():
    try:
        log(log.INFO, "Verification code sent successfully")
        flash("Verification code sent successfully")
        return {"status": "success"}, 200
    except Exception as e:
        log(log.ERROR, "Error sending verification code: [%s]", e)
        flash("Error sending verification code")
        return {"status": "error"}, 500


@chat_blueprint.route("/check", methods=["GET", "POST"])
def check():
    verification_code = request.args.get("verification_code")

    return render_template(
        "chat/chat_check.html",
    )


@chat_blueprint.route("/sms", methods=["GET", "POST"])
def sms():
    # Twilio
    account_sid = app.config["TWILIO_ACCOUNT_SID"]
    auth_token = app.config["TWILIO_AUTH_TOKEN"]
    sender = app.config["TWILIO_PHONE_NUMBER"]
    receiver = request.args.get("chat_phone")
    client = Client(account_sid, auth_token)

    message = client.messages.create(from_=sender, body="Twilio testing", to="+380934323377")

    log(log.INFO, "Message sent: [%s]", message)

    return render_template(
        "chat/chat_sms.html",
    )
