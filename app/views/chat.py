from typing import Any
from datetime import datetime
from flask import request, Blueprint, render_template
from flask_login import login_required, current_user
from app import models as m, db
from app import schema as s

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
        "chat/chat_01.html",
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
        "chat/chat_02.html",
        now=now_str,
        room=room,
        user=user,
    )


@chat_blueprint.route("/check", methods=["GET", "POST"])
def check():
    return render_template(
        "chat/chat_check.html",
    )
