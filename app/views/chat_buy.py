from datetime import datetime
import requests
import base64
import json
import os

from psycopg2 import IntegrityError

from flask import request, Blueprint, render_template, current_app as app, url_for
from flask_login import current_user, login_required

from app import controllers as c, schema as s, models as m, forms as f, db, pagarme_client
from app.logger import log
from app import mail_controller
from app.controllers.jinja_globals import transactions_last_month
from test_flask.assets.pagarme.webhook_response import WEBHOOK_RESPONSE

from config import config


CFG = config()
DEVELOPMENT_BASE_URL = os.environ.get("SERVER_NAME")
LOCAL_WEBHOOK_URL = f"http://{DEVELOPMENT_BASE_URL}/pay/webhook"

chat_buy_blueprint = Blueprint("buy", __name__, url_prefix="/buy")


@chat_buy_blueprint.route("/get_event_name", methods=["GET", "POST"])
def get_event_name():
    params = c.validate_event_buy_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.renew_search:
        c.save_message("Choose action", "Renew search", room)
        log(log.ERROR, "Renew search")
        return render_template(
            "chat/buy/event_name.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No event name provided: [%s]", params.user_message)
        return render_template(
            "chat/buy/event_name.html",
            error_message="No event date provided. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    c.save_message(
        "Great! To get started, could you please write below name of the event you're looking for?",
        f"{params.user_message}",
        room,
    )

    events = c.get_event_by_name_bard(params, room)

    if not events:
        log(log.INFO, "Events not found: [%s]", params.user_message)
        return render_template(
            "chat/buy/event_not_found.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    first_event: m.Event = events[0]
    if len(events) == 1:
        log(log.INFO, "Only 1 event found: [%s]", params.user_message)

        tickets = c.get_tickets_by_event(first_event, room)
        if not tickets:
            log(log.ERROR, "Tickets not found: [%s]", params.user_message)
            return render_template(
                "chat/buy/ticket_not_found.html",
                room=room,
                now=c.utcnow_chat_format(),
                event_unique_id=first_event.unique_id,
            )

        global_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
        tickets_cheapest = c.get_sorted_tickets(
            tickets,
            params.tickets_show_all,
            global_settings.tickets_sorting_by,
        )

        log(log.INFO, "Tickets found: [%s]", tickets)
        return render_template(
            "chat/buy/ticket_list.html",
            event_unique_id=first_event.unique_id,
            room=room,
            now=c.utcnow_chat_format(),
            tickets=tickets_cheapest,
            tickets_all_length=len(tickets),
            tickets_per_chat=app.config["TICKETS_PER_CHAT"],
            tickets_show_all=params.tickets_show_all,
        )

    locations = c.get_locations_by_events(events, room)
    if not locations:
        log(log.ERROR, "Locations not found: [%s]", params.user_message)
        return render_template(
            "chat/buy/ticket_not_found.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if len(locations) == 1:
        log(log.INFO, "Only 1 location found: [%s]", params.user_message)
        return render_template(
            "chat/buy/ticket_date.html",
            events=events,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/buy/location_list.html",
        event_unique_id=first_event.unique_id,
        events=events,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_buy_blueprint.route("/get_events_by_location")
def get_events_by_location():
    try:
        params = s.ChatBuyEventParams.model_validate(dict(request.args))
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

    if not params.location_unique_id:
        log(log.ERROR, "No location unique id provided: [%s]", params.location_unique_id)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.event_name:
        log(log.ERROR, "No event name provided: [%s]", params.event_name)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    events = c.get_events_by_location_event_name(params, room)

    if not events:
        log(log.INFO, "Events not found: [%s]", params.user_message)
        return render_template(
            "chat/buy/ticket_not_found.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    first_event: m.Event = events[0]
    if len(events) == 1:
        log(log.INFO, "Only 1 event found: [%s]", params.event_name)

        tickets = c.get_tickets_by_event(first_event, room)
        if not tickets:
            log(log.ERROR, "Tickets not found: [%s]", params.user_message)
            return render_template(
                "chat/buy/ticket_not_found.html",
                room=room,
                now=c.utcnow_chat_format(),
                event_unique_id=first_event.unique_id,
            )

        global_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
        tickets_cheapest = c.get_sorted_tickets(
            tickets,
            params.tickets_show_all,
            global_settings.tickets_sorting_by,
        )

        log(log.INFO, "Tickets found: [%s]", tickets)
        return render_template(
            "chat/buy/ticket_list.html",
            event_unique_id=first_event.unique_id,
            room=room,
            now=c.utcnow_chat_format(),
            tickets=tickets_cheapest,
            tickets_all_length=len(tickets),
            tickets_per_chat=app.config["TICKETS_PER_CHAT"],
            tickets_show_all=params.tickets_show_all,
        )

    return render_template(
        "chat/buy/ticket_date.html",
        events=events,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_buy_blueprint.route("/get_tickets")
def get_tickets():
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

    if not params.event_unique_id:
        log(log.ERROR, "No event unique id provided: [%s]", params.event_unique_id)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    tickets = c.get_tickets_by_event_id(params, room)

    if not tickets:
        log(log.ERROR, "Tickets not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/buy/ticket_not_found.html",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    if params.add_ticket:
        c.save_message(
            "Got it! Do you want to buy another one or proceed to purchase?",
            "Add ticket",
            room,
        )

    if params.from_date_template:
        event_date_time = tickets[0].event.date_time if tickets[0].event.date_time else datetime.now()
        event_time = event_date_time.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])
        c.save_message(
            "Sure! Please, choose available options:",
            f"{tickets[0].event.name}, {event_time}",
            room,
        )

    if params.tickets_show_all:
        c.save_message(
            f"Great news! We have found {len(tickets)} available options",
            "All tickets",
            room,
        )

    global_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
    tickets_cheapest = c.get_sorted_tickets(
        tickets,
        params.tickets_show_all,
        global_settings.tickets_sorting_by,
    )

    return render_template(
        "chat/buy/ticket_list.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
        tickets=tickets_cheapest,
        tickets_show_all=params.tickets_show_all,
        tickets_per_chat=app.config["TICKETS_PER_CHAT"],
        tickets_all_length=len(tickets),
    )


@chat_buy_blueprint.route("/booking_ticket")
def booking_ticket():
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
    form: f.ChatFileUploadForm = f.ChatFileUploadForm()

    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )
    if not params.ticket_unique_id:
        log(log.ERROR, "No ticket id provided: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/buy/ticket_not_found.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not current_user.is_authenticated:
        log(log.ERROR, "User not authenticated: [%s]", current_user)
        return render_template(
            "chat/registration/login_form.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not current_user.activated:
        log(log.ERROR, "User not activated: [%s]", current_user)
        return render_template(
            "chat/registration/passport_identity_number.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=current_user.uuid,
            form=form,
        )

    transactions_last_month_number = transactions_last_month(current_user)
    global_fee_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
    if transactions_last_month_number > global_fee_settings.buying_limit:
        log(log.ERROR, "Transactions limit reached: [%s]", transactions_last_month_number)
        c.save_message(
            "Unfortunately in order to avoid frauds we have to limit transactions. You can't perform more than 6 per month.",
            f"Transactions last month: {transactions_last_month_number}",
            room,
        )
        return render_template(
            "chat/buy/transactions_limit.html",
            error_message="You have reached the limit of 6 transactions per month",
            now=c.utcnow_chat_format(),
            room=room,
        )

    ticket = c.book_ticket(params.ticket_unique_id, current_user, room, global_fee_settings.limit_per_event)

    if isinstance(ticket, s.BookTicketError):
        log(log.ERROR, "Booking ticket error: [%s]", ticket.error_message)
        return render_template(
            "chat/buy/transactions_limit.html",
            error_message=ticket.error_message,
            room=room,
            now=c.utcnow_chat_format(),
        )

    try:
        db.session.commit()
        log(log.INFO, f"Ticket {ticket.unique_id} updated")
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Ticket is not updated: [%s]", e)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong, please choose event again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/buy/ticket_ask_another_one.html",
        event_unique_id=ticket.event.unique_id,
        room=room,
        now=c.utcnow_chat_format(),
        ticket_unique_id=ticket.unique_id,
    )


@chat_buy_blueprint.route("/payment")
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
        f"Awesome! The cost for ticket(s) is {total_prices.net}. Price for service is {total_prices.service}. Total price is {total_prices.total}. Please proceed to payment",
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


@chat_buy_blueprint.route("/subscribe_on_event")
def subscribe_on_event():
    params = c.validate_buy_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.event_unique_id:
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong, please choose event again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not current_user.is_authenticated and not params.has_email:
        log(log.INFO, "User unauthorized without email: [%s]", params.has_email)
        return render_template(
            "chat/buy/email_for_subscribe.html",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    if not current_user.is_authenticated and params.has_email and not params.user_message:
        log(log.INFO, "User unauthorized. Email is not provided: [%s]", params.user_message)
        return render_template(
            "chat/buy/email_for_subscribe.html",
            error_message="Please provide your email",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    if not current_user.is_authenticated:
        if not params.user_message:
            log(log.INFO, "User unauthorized. Email is not provided: [%s]", params.user_message)
            return render_template(
                "chat/buy/email_for_subscribe.html",
                error_message="Please provide your email",
                room=room,
                now=c.utcnow_chat_format(),
                event_unique_id=params.event_unique_id,
            )
        user = c.create_user(params.user_message)

        try:
            db.session.commit()
            log(log.INFO, "User created: [%s]", user)
        except IntegrityError as e:
            db.session.rollback()
            log(log.ERROR, "User is not created: [%s]", e)
            return render_template(
                "chat/buy/event_name.html",
                error_message="Something went wrong, please choose event again",
                room=room,
                now=c.utcnow_chat_format(),
            )

    event = c.subscribe_event(params.event_unique_id, user)

    if not event:
        log(log.ERROR, "Subscribe not found: [%s]", event)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong, please choose event again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if os.environ.get("APP_ENV") == "development":
        url = url_for(
            "auth.activate",
            reset_password_uuid=user.uuid,
            _external=True,
        )
    else:
        if os.environ.get("SERVER_TYPE") == "production":
            base_url = app.config["PRODUCTION_BASE_URL"]
        else:
            base_url = app.config["STAGING_BASE_URL"]
        url = f"{base_url}activated/{user.uuid}"

    mail_controller.send_email(
        (user,),
        f"Subscription to {CFG.APP_NAME}",
        render_template(
            "email/email_confirm_subscribe.htm",
            user=user,
            event_name=event.name,
            url=url,
        ),
    )

    return render_template(
        "chat/buy/subscribe_success.html",
        room=room,
        now=c.utcnow_chat_format(),
        email=current_user.email if current_user.is_authenticated else user.email,
    )


def compute_total_price(cart_tickets: list[m.Ticket]) -> int:
    return sum([ticket.price_gross for ticket in cart_tickets if ticket.price_gross])


@chat_buy_blueprint.route("/pagar", methods=["GET", "POST"])
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
