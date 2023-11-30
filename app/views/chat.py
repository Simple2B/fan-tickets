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
    # new_message_text = request.form.get("message")

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
    return render_template(
        "chat/chat_check.html",
    )


@chat_blueprint.route("/check", methods=["GET", "POST"])
def check():
    return render_template(
        "chat/chat_check.html",
    )
