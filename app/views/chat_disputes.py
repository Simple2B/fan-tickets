from datetime import datetime, timedelta
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from flask_mail import Message
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

    room = m.Room(
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
