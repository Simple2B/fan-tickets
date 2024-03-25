from datetime import datetime
import os

from psycopg2 import IntegrityError

from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user

from app import controllers as c, schema as s, models as m, forms as f, db
from app.logger import log
from app.controllers.jinja_globals import transactions_last_month

from config import config


CFG = config()
DEVELOPMENT_BASE_URL = os.environ.get("SERVER_NAME")
LOCAL_WEBHOOK_URL = f"http://{DEVELOPMENT_BASE_URL}/pay/webhook"

ticket_blueprint = Blueprint("buy_ticket", __name__, url_prefix="/ticket")


@ticket_blueprint.route("/get_by_event")
def get_by_event():
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


@ticket_blueprint.route("/booking")
def booking():
    try:
        params = s.ChatBuyTicketParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    form: f.ChatFileUploadForm = f.ChatFileUploadForm()

    room = c.get_room(params.room_unique_id)

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
            ticket_unique_id=params.ticket_unique_id,
        )

    if not current_user.activated:
        log(log.ERROR, "User not activated: [%s]", current_user)
        return render_template(
            "chat/registration/passport_identity_number.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=current_user.uuid,
            form=form,
            ticket_unique_id=params.ticket_unique_id,
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
            error_message="You have reached the limit of transactions per month",
            now=c.utcnow_chat_format(),
            room=room,
            buying=True,
        )

    ticket = c.book_ticket(params.ticket_unique_id, current_user, room, global_fee_settings.limit_per_event)

    if isinstance(ticket, s.BookTicketError):
        log(log.ERROR, "Booking ticket error: [%s]", ticket.error_message)
        return render_template(
            "chat/buy/transactions_limit.html",
            error_message=ticket.error_message,
            buying=True,
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


@ticket_blueprint.route("/booking_from_web", methods=["GET"])
def booking_from_web():
    params = s.ChatBuyTicketWithoutRequiredParams.model_validate(dict(request.args))
    room = m.Room(
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    return render_template(
        "chat/buy/booking_ticket_from_web.html",
        room=room,
        now=c.utcnow_chat_format(),
        ticket_unique_id=params.ticket_unique_id,
    )
