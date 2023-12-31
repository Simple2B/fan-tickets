from datetime import datetime
import os
from flask import request, Blueprint, render_template, current_app as app, url_for
from flask_login import current_user, login_required
from flask_mail import Message
from psycopg2 import IntegrityError

from app import controllers as c
from app import schema as s
from app import models as m, db, mail
from app import forms as f
from app.logger import log
from config import config

CFG = config()

chat_buy_blueprint = Blueprint("buy", __name__, url_prefix="/buy")


@chat_buy_blueprint.route("/get_event_name", methods=["GET", "POST"])
def get_event_name():
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

    if params.renew_search:
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

    events = c.get_events_by_event_name(params.user_message, room)

    if not events:
        log(log.INFO, "Events not found: [%s]", params.user_message)
        return render_template(
            "chat/buy/ticket_not_found.html",
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

        tickets_cheapest = c.get_cheapest_tickets(
            tickets,
            room,
            params.tickets_show_all,
            params.add_ticket,
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

    c.save_message(
        "Great! To get started, could you please write below name of the event you're looking for?",
        f"{params.user_message}",
        room,
    )

    return render_template(
        "chat/buy/location_list.html",
        event_unique_id=first_event.unique_id,
        locations=locations,
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

        tickets_cheapest = c.get_cheapest_tickets(
            tickets,
            room,
            params.tickets_show_all,
            params.add_ticket,
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

    tickets = c.get_tickets_by_event_id(params.event_unique_id, room)

    if not tickets:
        log(log.ERROR, "Tickets not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    tickets_cheapest = c.get_cheapest_tickets(
        tickets,
        room,
        params.tickets_show_all,
        params.add_ticket,
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

    ticket = c.book_ticket(params.ticket_unique_id, current_user, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/buy/get_event_name.html",
            error_message="Something went wrong, please choose event again",
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
        f"Awesome! The cost for ticket is {total_prices.net}. Price for service is {total_prices.service}. Total price is {total_prices.total}. Please proceed to payment",
        "Payment",
        room,
    )
    return render_template(
        "chat/buy/payment.html",
        room=room,
        now=c.utcnow_chat_format(),
        total_prices=total_prices,
        form=f.OrderCreateForm(),
    )


@chat_buy_blueprint.route("/subscribe_on_event")
def subscribe_on_event():
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

    if current_user.is_authenticated:
        c.subscribe_event(params.event_unique_id, current_user)
    else:
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

        msg = Message(
            subject="Congratulations! You have successfully register on {CFG.APP_NAME}",
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email],
        )
        # TODO: add production url
        if os.environ.get("APP_ENV") == "development":
            url = url_for(
                "auth.activate",
                reset_password_uid=user.unique_id,
                _external=True,
            )
        else:
            base_url = app.config["STAGING_BASE_URL"]
            url = f"{base_url}activated/{user.unique_id}"

        msg.html = render_template(
            "email/confirm.htm",
            user=user,
            url=url,
        )
        mail.send(msg)

        c.subscribe_event(params.event_unique_id, user)

    try:
        db.session.commit()
        log(log.INFO, "Subscribe on event: [%s], [%s]", params.event_unique_id, current_user.email)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Subscribe on event failed: [%s]", e)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong, please choose event again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/buy/subscribe_success.html",
        room=room,
        now=c.utcnow_chat_format(),
        email=current_user.email if current_user.is_authenticated else user.email,
    )


def compute_total_price(cart_tickets: list[m.Ticket]) -> float:
    return sum([ticket.price_gross for ticket in cart_tickets])


def clear_message_history(room: m.Room) -> None:
    if not room:
        log(log.ERROR, "Room not found: [%s]", room)
        return

    messages_query = m.Message.select().where(m.Message.room_id == room.id)
    messages = db.session.scalars(messages_query).all()

    msg = Message(
        subject=f"Today's chat history {datetime.now().strftime(app.config['DATE_CHAT_HISTORY_FORMAT'])}",
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[current_user.email],
    )
    msg.html = render_template(
        "email/chat_history.htm",
        user=current_user,
        messages=messages,
    )
    mail.send(msg)

    for message in messages:
        db.session.delete(message)
    db.session.commit()
    return


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
