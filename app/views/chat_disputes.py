from datetime import datetime, timedelta
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from flask_mail import Message
from flask_sse import sse
from app import models as m, db, mail
from app.controllers import utcnow_chat_format, save_message
from app.logger import log
from config import config

CFG = config()

chat_disputes_blueprint = Blueprint("disputes", __name__, url_prefix="/disputes")


@chat_disputes_blueprint.route("/", methods=["GET"])
def start_dispute():
    payment_id = request.args.get("payment_id")

    payment_query = m.Payment.select().where(m.Payment.id == payment_id)
    payment: m.Payment = db.session.scalar(payment_query)

    room_query = m.Room.select().where(m.Room.ticket_id == payment.ticket_id)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        room = m.Room(
            type_of=m.RoomType.DISPUTE.value,
            seller_id=payment.ticket.seller_id,
            buyer_id=current_user.id,
            ticket_id=payment.ticket_id,
        ).save()

    # save_message(
    #     "Message from the bot",
    #     "Message from the user",
    #     # room,
    # )

    return render_template(
        "disputes/start_dispute.html",
        now=utcnow_chat_format(),
        room=room,
    )


@chat_disputes_blueprint.route("/send/<room_unique_id>")
@login_required
def send_message():
    sse.publish(
        {"message": "Hello!"},
        type="greeting",
        channel="room_unique_id",
    )
    return "Message sent!"
