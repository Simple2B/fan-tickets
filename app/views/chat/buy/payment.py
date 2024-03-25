from datetime import datetime
import requests
import base64
import json
import os

from psycopg2 import IntegrityError

from flask import request, Blueprint, render_template
from flask_login import current_user, login_required

from app import controllers as c, schema as s, models as m, forms as f, db, pagarme_client
from app.logger import log
from test_flask.assets.pagarme.webhook_response import WEBHOOK_RESPONSE

from config import config


CFG = config()
DEVELOPMENT_BASE_URL = os.environ.get("SERVER_NAME")
LOCAL_WEBHOOK_URL = f"http://{DEVELOPMENT_BASE_URL}/pay/webhook"

payment_blueprint = Blueprint("payment", __name__, url_prefix="/payment")


@payment_blueprint.route("/payment")
@login_required
def payment():
    try:
        params = s.ChatBuyTicketParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    total_prices = c.calculate_total_price(current_user)

    if not total_prices:
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong, please choose event again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    try:
        db.session.commit()
        log(log.INFO, "Tickets updated")
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Tickets are not updated: [%s]", e)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong, please choose event again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.ask_payment:
        c.save_message("Got it! Do you want to buy another one or proceed to purchase?", "Purchase", room)
        return render_template(
            "chat/buy/ticket_accept_purchase.html",
            room=room,
            now=c.utcnow_chat_format(),
            total_prices=total_prices,
        )

    c.save_message(
        f"Awesome! The cost for ticket(s) is  {total_prices.total}. Please proceed to payment",
        "Payment",
        room,
    )

    if not current_user.pagarme_id:
        phone_data = pagarme_client.generate_customer_phone(current_user.phone)
        phones_data = s.PagarmeCustomerPhones(
            mobile_phone=phone_data,
        )

        customer_data = s.PagarmeCustomerCreate(
            name=current_user.name,
            birthdate=current_user.birth_date_string,
            code=current_user.uuid,
            email=current_user.email,
            document=current_user.document_identity_number,
            phones=phones_data,
        )

        pagarme_customer = pagarme_client.create_customer(customer_data)

        assert pagarme_customer

        current_user.pagarme_id = pagarme_customer.id
        current_user.save()

    data = s.PagarmeCreateOrderPix(
        items=[
            s.PagarmeItem(
                amount=int(total_prices.total) * 100,
                description=total_prices.unique_ids,
                category="Concert Event",
            )
        ],
        customer_id=current_user.pagarme_id,
        payments=[
            s.PagarmePaymentPix(
                expires_in=30,
                payment_method="pix",
                billing_address_editable=False,
                customer_editable=False,
                accepted_payment_methods=["pix"],
                success_url="https://fan-ticket.simple2b.net/pay/webhook",
                Pix=s.PagarmePixData(
                    expires_in=115576000,
                ),
            )
        ],
    )
    resp = pagarme_client.create_order_pix(data)
    response_dict = json.loads(resp.json())
    qr_code_url = response_dict["charges"][0]["last_transaction"]["qr_code_url"]
    qr_to_copy = response_dict["charges"][0]["last_transaction"]["qr_code"]
    if os.environ.get("APP_ENV") == "testing":
        with open("test_flask/assets/pagarme/qr.png", "rb") as qr_file:
            qr = qr_file.read()
            qr_url = "https://api.pagar.me/core/v5/transactions/tran_236wYQRSPUnBwb08/qrcode?payment_method=pix"
    else:
        response = requests.get(qr_code_url)
        assert response.status_code == 200, f"Failed to retrieve QR code image. Status code: {response.status_code}"
        qr = response.content
        qr_url = response.url
    qr_base64 = base64.b64encode(qr).decode()

    if os.environ.get("APP_ENV") == "development":
        webhook_response = s.PagarmePaidWebhook.model_validate(WEBHOOK_RESPONSE)
        webhook_response.data.customer.code = current_user.uuid
        webhook_response.data.items[0].description = total_prices.unique_ids
        testing_webhook = requests.post(LOCAL_WEBHOOK_URL, json=webhook_response.model_dump())
        log(log.INFO, f"Testing webhook response: {testing_webhook.status_code}")

    return render_template(
        "chat/buy/payment.html",
        room=room,
        qr=qr_base64,
        qr_to_copy=qr_to_copy,
        qr_url=qr_url,
        now=c.utcnow_chat_format(),
        total_prices=total_prices,
        form=f.OrderCreateForm(),
    )


@payment_blueprint.route("/pagar", methods=["GET", "POST"])
def pagar():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    event_unique_id = request.args.get("event_unique_id")
    ticket_unique_id = request.args.get("ticket_unique_id")
    room_unique_id = request.args.get("room_unique_id")
    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/buy/events_04_tickets.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )
    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket = db.session.scalar(ticket_query)
    event_query = m.Event.select().where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)
    return render_template(
        "chat/buy/tickets_07_pagar.html",
        room=room,
        event=event,
        ticket=ticket,
    )
