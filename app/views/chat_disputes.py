from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required

# from flask_sse import sse
from app import models as m, db
from app.controllers import utcnow_chat_format
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
        log(log.INFO, "Creating dispute room for payment [%s]", payment.id)
        room = m.Room(
            type_of=m.RoomType.DISPUTE.value,
            seller_id=payment.ticket.seller_id,
            buyer_id=current_user.id,
            ticket_id=payment.ticket_id,
        ).save(False)
        db.session.flush()
        m.Message(
            sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
            room_id=room.id,
            text="If you want to start a dispute, please describe the issue",
        ).save(False)
        db.session.commit()

        return render_template(
            "admin/start_dispute.html",
            now=utcnow_chat_format(),
            room=room,
        )

    log(log.INFO, "Dispute room already exists for payment [%s]", payment.id)
    return render_template(
        "admin/messages.html",
        now=utcnow_chat_format(),
        room=room,
    )


@chat_disputes_blueprint.route("/send")
@login_required
def send_message():
    # sse.publish(
    #     {"message": "Hello!"},
    #     type="greeting",
    #     channel="room_unique_id",
    # )
    room_unique_id = request.args.get("room_unique_id")
    user_message = request.args.get("user_message")
    if room_unique_id:
        room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
        room: m.Room = db.session.scalar(room_query)
    if user_message:
        m.Message(
            room_id=room.id,
            sender_id=current_user.id,
            text=user_message,
        ).save()
    return render_template(
        "admin/messages.html",
        now=utcnow_chat_format(),
        room=room,
    )
