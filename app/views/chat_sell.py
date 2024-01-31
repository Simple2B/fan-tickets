from datetime import datetime
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from psycopg2 import IntegrityError
from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db
from app.controllers.jinja_globals import cut_seconds
from app.logger import log
from config import config

CFG = config()

chat_sell_blueprint = Blueprint("sell", __name__, url_prefix="/sell")


@chat_sell_blueprint.route("/get_event_category")
@login_required
def get_event_category():
    try:
        params = s.ChatSellEventParams.model_validate(dict(request.args))
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

    category_name = db.session.scalar(
        m.Category.select().where(m.Category.unique_id == params.event_category_id).with_only_columns(m.Category.name)
    )

    if not category_name:
        category_name = "Others"

    c.save_message(
        "Great! What is the category of event are you selling tickets for?",
        f"{category_name}",
        room,
    )

    log(log.INFO, "Event category: [%s]", params.event_category_id)
    return render_template(
        "chat/sell/event_name.html",
        event_category_id=params.event_category_id if params.event_category_id else category_name,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_event_name")
@login_required
def get_event_name():
    try:
        params = s.ChatSellEventParams.model_validate(dict(request.args))
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

    if not params.event_category_id:
        log(log.ERROR, "No event category provided: [%s]", params.event_category_id)
        return render_template(
            "chat/sell/event_category.html",
            error_message="No event category provided. Please add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No event name provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_name.html",
            error_message="No event name provided. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
            event_category_id=params.event_category_id,
        )

    events = c.get_event_by_name_bard(params)

    # TODO: move the message from the user with the chosen event to the place where the event is chosen
    c.save_message(
        "Please, input official event name (matching the official website)",
        f"{params.user_message}",
        room,
    )

    if events:
        return render_template(
            "chat/sell/event_approve.html",
            events=events,
            event_category_id=params.event_category_id,
            room=room,
            now=c.utcnow_chat_format(),
        )

    else:
        return render_template(
            "chat/sell/event_url.html",
            event_name=params.user_message,
            event_category_id=params.event_category_id,
            room=room,
            now=c.utcnow_chat_format(),
        )


@chat_sell_blueprint.route("/get_event_url")
@login_required
def get_event_url():
    try:
        params = s.ChatSellEventParams.model_validate(dict(request.args))
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

    if not params.event_category_id:
        log(log.ERROR, "No event category provided: [%s]", params.event_category_id)
        return render_template(
            "chat/sell/event_category.html",
            error_message="No event category provided. Please add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.create_event:
        return render_template(
            "chat/sell/event_url.html",
            event_name=params.event_name,
            event_category_id=params.event_category_id,
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.event_name:
        log(log.ERROR, "No event name provided: [%s]", params.event_name)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
            event_category_id=params.event_category_id,
        )

    if not params.user_message:
        log(log.ERROR, "No event url provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_name.html",
            error_message="No event url provided. Please add event url",
            room=room,
            now=c.utcnow_chat_format(),
            event_category_id=params.event_category_id,
        )

    event = c.create_event(params, room, current_user)

    c.save_message(
        "Please provide us with a link of event👇",
        f"{params.user_message[8:25]}...",
        room,
    )

    return render_template(
        "chat/sell/event_location.html",
        event_unique_id=event.unique_id,
        event_category_id=params.event_category_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_event_location")
@login_required
def get_event_location():
    try:
        params = s.ChatSellEventParams.model_validate(dict(request.args))
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
        log(log.ERROR, "No event unique id: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_category.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No event location provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_location.html",
            error_message="No event location provided, please, add event location",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    success = c.add_event_location(params)

    if not success:
        log(log.ERROR, "Event not found, params: [%s]", params)
        return render_template(
            "chat/chat_window.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    c.save_message(
        "Got it! Please provide the city of the event.",
        f"{params.user_message}",
        room,
    )

    return render_template(
        "chat/sell/event_venue.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_event_venue")
@login_required
def get_event_venue():
    try:
        params = s.ChatSellEventParams.model_validate(dict(request.args))
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
        log(log.ERROR, "No event unique id: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_category.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No event location provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_location.html",
            error_message="No event location provided, please, add event location",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    success = c.add_event_venue(params)

    if not success:
        log(log.ERROR, "Event not found, params: [%s]", params)
        return render_template(
            "chat/chat_window.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    c.save_message(
        "Nice! Please provide the location name.",
        f"{params.user_message}",
        room,
    )

    return render_template(
        "chat/sell/event_date.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_event_date")
@login_required
def get_event_date():
    try:
        params = s.ChatSellEventParams.model_validate(dict(request.args))
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
        log(log.ERROR, "No event unique id: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_category.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No event date provided, please, add event date: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_date.html",
            error_message="No event date provided, please, add event date",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    try:
        event_date = datetime.strptime(params.user_message, app.config["CHAT_USER_FORMAT"])
    except ValueError as e:
        log(log.ERROR, "Invalid event date. Error: [%s], date: [%s]", e, params.user_message)
        return render_template(
            "chat/sell/event_date.html",
            error_message="Invalid event date, please enter a date in the format DD/MM/YYYY",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    success = c.add_event_date(params, event_date)

    if not success:
        log(log.ERROR, "Event not found, params: [%s]", params)
        return render_template(
            "chat/chat_window.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    c.save_message(
        "Nice! Please specify the date",
        f"{params.user_message}",
        room,
    )

    return render_template(
        "chat/sell/event_time.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_event_time")
@login_required
def get_event_time():
    try:
        params = s.ChatSellEventParams.model_validate(dict(request.args))
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
        log(log.ERROR, "No event unique id: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_category.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No event time provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_location.html",
            error_message="No event time provided, please, add event time",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    try:
        event_time = datetime.strptime(params.user_message, "%H:%M").time()
    except ValueError as e:
        log(log.ERROR, "Invalid event time. Error: [%s], time: [%s]", e, params.user_message)
        return render_template(
            "chat/sell/event_time.html",
            error_message="Invalid event time, please enter a time in the format HH:MM",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    success = c.add_event_time(params, event_time)

    if not success:
        log(log.ERROR, "Event not found, params: [%s]", params)
        return render_template(
            "chat/chat_window.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_quantity.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_quantity")
@login_required
def get_ticket_quantity():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/sell/ticket_quantity.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/sell/ticket_quantity.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.event_unique_id:
        log(log.ERROR, "Not found event_unique_id: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/ticket_quantity.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.tickets_quantity_answer:
        log(log.INFO, "Tickets quantity answer: [%s]", params.tickets_quantity_answer)

        event_query = m.Event.select().where(m.Event.unique_id == params.event_unique_id)
        event: m.Event = db.session.scalar(event_query)

        if not event:
            log(log.ERROR, "Event not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/ticket_quantity.html",
                error_message="Event identifier is not valid",
                now=c.utcnow_chat_format(),
            )

        ticket = c.create_ticket(params, room)

        if params.tickets_quantity_answer == "2":
            return render_template(
                "chat/sell/ticket_separate_sell.html",
                ticket_unique_id=ticket.unique_id,
                room=room,
                now=c.utcnow_chat_format(),
                event_unique_id=params.event_unique_id,
            )
        types = [t.value.replace("_", " ").title() for t in m.TicketType]
        return render_template(
            "chat/sell/ticket_type.html",
            ticket_unique_id=ticket.unique_id,
            room=room,
            types=types,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    return render_template(
        "chat/sell/ticket_quantity.html",
        room=room,
        event_unique_id=params.event_unique_id,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_separate_sell")
@login_required
def get_ticket_separate_sell():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/sell/ticket_separate_sell.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/sell/ticket_separate_sell.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.event_unique_id:
        log(log.ERROR, "Not found event_unique_id: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/ticket_ticket_separate_sell.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.ticket_paired is not None:
        log(log.INFO, "Tickets paired answer: [%s]", params.ticket_paired)
        user_message = "Yes" if params.ticket_paired else "No"
        c.save_message(
            "Got it! Do you allow sell tickets separately? Choose or write below the answer",
            user_message,
            room,
        )

        ticket = c.create_paired_ticket(params, room)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.ticket_unique_id)
            return render_template(
                "chat/sell/ticket_separate_sell.html",
                error_message="Event identifier is not valid",
                now=c.utcnow_chat_format(),
            )

        types = [t.value.replace("_", " ").title() for t in m.TicketType]
        return render_template(
            "chat/sell/ticket_type.html",
            ticket_unique_id=ticket.unique_id,
            room=room,
            types=types,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    return render_template(
        "chat/sell/ticket_separate_sell.html",
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_type")
@login_required
def get_ticket_type():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found event_unique_id: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.ticket_type:
        log(log.ERROR, "No ticket type provided: [%s]", params.ticket_type)
        return render_template(
            "chat/sell/ticket_type.html",
            error_message="No ticket type provided, please, add ticket type",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    if not ticket:
        log(log.ERROR, "Event not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    try:
        ticket.ticket_type = params.ticket_type.replace(" ", "_").lower()
        db.session.commit()
        log(log.INFO, "Ticket type added: [%s]", ticket.unique_id)
        c.save_message(
            "Got it! What is the type of ticket are you selling?",
            f"{params.ticket_type}",
            room,
        )
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Error commit: [%s]", e)
        return render_template(
            "chat/sell/ticket_type.html",
            error_message="Form submitting error. Please add your ticket type again",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    ticket_categories = [t.value.replace("_", " ").title() for t in m.TicketCategory]
    return render_template(
        "chat/sell/ticket_category.html",
        room=room,
        ticket_unique_id=ticket.unique_id,
        ticket_categories=ticket_categories,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_category")
@login_required
def get_ticket_category():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.ticket_category:
        log(log.ERROR, "No ticket category provided: [%s]", params.ticket_category)
        return render_template(
            "chat/sell/ticket_category.html",
            error_message="No ticket category provided, please, add ticket category",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    ticket = c.add_ticket_category(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    try:
        db.session.commit()
        log(log.INFO, "Ticket category added: [%s]", ticket.unique_id)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Error commit: [%s]", e)
        return render_template(
            "chat/sell/ticket_category.html",
            error_message="Form submitting error. Please add your ticket category again",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    return render_template(
        "chat/sell/ticket_has_section.html",
        room=room,
        event_unique_id=params.event_unique_id,
        ticket_unique_id=ticket.unique_id,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/has_ticket_section")
@login_required
def has_ticket_section():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.ticket_has_section is False:
        c.save_message("Does this ticket have a section?", "Ticket does not have a section", room)
        log(log.ERROR, "Ticket has no section: [%s]", params.ticket_has_section)
        return render_template(
            "chat/sell/ticket_has_queue.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    c.save_message("Does this ticket have a section?", "Ticket has a section", room)
    log(log.ERROR, "Ticket has a section: [%s]", params.ticket_has_section)
    return render_template(
        "chat/sell/ticket_get_section.html",
        room=room,
        event_unique_id=params.event_unique_id,
        ticket_unique_id=params.ticket_unique_id,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_section")
@login_required
def get_ticket_section():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.user_message:
        ticket = c.add_ticket_section(params, room)
        log(log.INFO, "Tickets section answer: [%s]", params.ticket_section)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, add event name",
                room=room,
                now=c.utcnow_chat_format(),
            )

        return render_template(
            "chat/sell/ticket_has_queue.html",
            ticket_unique_id=params.ticket_unique_id,
            event_unique_id=params.event_unique_id,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_get_section.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/has_ticket_queue")
@login_required
def has_ticket_queue():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.ticket_has_queue is False:
        c.save_message("Does this ticket have a queue?", "Ticket does not have a queue", room)
        log(log.ERROR, "Ticket has no queue: [%s]", params.ticket_has_queue)
        return render_template(
            "chat/sell/ticket_has_seat.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    c.save_message("Does this ticket have a queue?", "Ticket has a queue", room)
    log(log.INFO, "Ticket has a queue: [%s]", params.user_message)
    return render_template(
        "chat/sell/ticket_get_queue.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_queue")
@login_required
def get_ticket_queue():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.user_message:
        ticket = c.add_ticket_queue(params, room)
        log(log.INFO, "Ticket queue added: [%s]", ticket.queue)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, add event name",
                room=room,
                now=c.utcnow_chat_format(),
            )

    return render_template(
        "chat/sell/ticket_has_seat.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/has_ticket_seat")
@login_required
def has_ticket_seat():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.ticket_has_seat:
        c.save_message("Does this ticket have a seat?", "Ticket does not have a seat", room)
        log(log.ERROR, "Ticket has no seat: [%s]", params.ticket_has_seat)
        return render_template(
            "chat/sell/ticket_notes.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    c.save_message("Does this ticket have a seat?", "Ticket has a seat", room)
    log(log.INFO, "Ticket has a seat: [%s]", params.ticket_has_seat)

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    return render_template(
        "chat/sell/ticket_get_seat.html",
        ticket_unique_id=params.ticket_unique_id,
        ticket_paired=ticket.is_paired,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_seat")
@login_required
def get_ticket_seat():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.user_message:
        ticket = c.add_ticket_seat(params, room)
        log(log.INFO, "Ticket seat added: [%s]", ticket.seat)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, add event name",
                room=room,
                now=c.utcnow_chat_format(),
            )

    return render_template(
        "chat/sell/ticket_notes.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_notes")
@login_required
def get_ticket_notes():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, input ticket details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.user_message:
        ticket = c.add_ticket_notes(params, room)
        log(log.INFO, "Ticket notes added: [%s]", ticket.description)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, input ticket details again",
                room=room,
                now=c.utcnow_chat_format(),
            )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    return render_template(
        "chat/sell/ticket_price.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        ticket_paired=ticket.is_paired,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_price")
@login_required
def get_ticket_price():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, input ticket details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.user_message:
        try:
            users_price = int(params.user_message)
        except ValueError as e:
            log(log.ERROR, "Invalid ticket price. Error: [%s], price: [%s]", e, params.user_message)
            return render_template(
                "chat/sell/ticket_price.html",
                error_message="Invalid ticket price, please enter a price in the format 100",
                room=room,
                now=c.utcnow_chat_format(),
                ticket_unique_id=params.ticket_unique_id,
            )
        ticket = c.add_ticket_price(params, room, users_price)
        log(log.INFO, "Ticket's price is set: [%s]", ticket.price_gross)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, input ticket details again",
                room=room,
                now=c.utcnow_chat_format(),
            )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    return render_template(
        "chat/sell/ticket_details.html",
        ticket_unique_id=ticket.unique_id,
        ticket=ticket,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_details")
@login_required
def get_ticket_details():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, input ticket details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    ticket_details = (
        f"Event: {ticket.event.name}\n"
        f"Location: {ticket.event.location.name}\n"
        f"Venue: {ticket.event.venue}\n"
        f"Date time: {cut_seconds(ticket.event.date_time)}\n"
        f"Ticket type: {ticket.ticket_type}\n"
        f"Ticket category: {ticket.ticket_category}\n"
        f"Ticket section: {ticket.section}\n"
        f"Ticket price net: {ticket.price_net}\n"
        f"Ticket price gross: {ticket.price_gross}\n"
        f"Ticket description: {ticket.description}"
    )
    c.save_message(ticket_details, "Got it", room)
    return render_template(
        "chat/sell/ticket_details.html",
        ticket_unique_id=params.ticket_unique_id,
        ticket=ticket,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/ticket_file_type")
@login_required
def get_ticket_file_type():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, input ticket details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.user_message == "PDF":
        log(log.INFO, "User choose PDF file type: [%s]", params.user_message)
        c.save_message("What version of ticket do you have?", "PDF", room)
        return render_template(
            "chat/sell/ticket_document.html",
            ticket_unique_id=params.ticket_unique_id,
            room=room,
            now=c.utcnow_chat_format(),
        )
    elif params.user_message == "wallet_id":
        log(log.INFO, "User choose wallet id file type: [%s]", params.user_message)
        c.save_message("What version of ticket do you have?", "Wallet id", room)
        return render_template(
            "chat/sell/ticket_wallet_id.html",
            ticket_unique_id=params.ticket_unique_id,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_file_type.html",
        ticket_unique_id=params.ticket_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_wallet_code")
@login_required
def get_wallet_code():
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request.args))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, input ticket details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if params.user_message:
        ticket = c.add_ticket_wallet_id(params, room)
        log(log.INFO, "Tickets wallet id added: [%s]", ticket.wallet_id)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, input ticket details again",
                room=room,
                now=c.utcnow_chat_format(),
            )

        return render_template(
            "chat/sell/ticket_posted.html",
            ticket_unique_id=params.ticket_unique_id,
            event_unique_id=params.event_unique_id,
            ticket_paired=params.ticket_paired,
            room=room,
            now=c.utcnow_chat_format(),
        )
    return render_template(
        "chat/sell/ticket_wallet_code.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        ticket_paired=params.ticket_paired,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_document", methods=["GET", "POST"])
@login_required
def get_ticket_document():
    if request.method == "GET":
        params_input = request.args
    else:
        params_input = request.values

    try:
        params = s.ChatSellTicketParams.model_validate(dict(params_input))
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
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, input ticket details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    form: f.ChatFileUploadForm = f.ChatFileUploadForm()
    if form.validate_on_submit():
        file = request.files.get("file")
        ticket = c.add_ticket_document(form, params, file, room)
        log(log.INFO, "Tickets PDF document is added: [%s]", ticket.file)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, input ticket details again",
                room=room,
                now=c.utcnow_chat_format(),
            )

        return render_template(
            "chat/sell/ticket_posted.html",
            ticket_unique_id=params.ticket_unique_id,
            event_unique_id=params.event_unique_id,
            ticket_paired=params.ticket_paired,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_document.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        ticket_paired=params.ticket_paired,
        room=room,
        form=form,
        now=c.utcnow_chat_format(),
    )
