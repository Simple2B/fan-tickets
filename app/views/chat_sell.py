from datetime import datetime
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from psycopg2 import IntegrityError
from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db
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

    events = c.get_event_by_name_bard(params.user_message)

    # TODO: move the message from the user with the chosen event to the plase where the event is chosen
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
        "Please provide us with a link of even👇",
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
        ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
        ticket: m.Ticket = db.session.scalar(ticket_query)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.ticket_unique_id)
            return render_template(
                "chat/sell/ticket_separate_sell.html",
                error_message="Event identifier is not valid",
                now=c.utcnow_chat_format(),
            )

        ticket.is_paired = params.ticket_paired
        ticket.save()
        log(log.INFO, "Ticket changed: [%s]. Redirecting to ticket type input.", ticket.unique_id)

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
        event_unique_id=params.event_unique_id,
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
            "chat/sell/ticket_queue.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

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
            "chat/sell/ticket_seat.html",
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
            "chat/sell/ticket_seat.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    c.save_message("Does this ticket have a seat?", "Ticket has a seat", room)
    log(log.INFO, "Ticket has a seat: [%s]", params.ticket_has_seat)
    return render_template(
        "chat/sell/ticket_get_seat.html",
        ticket_unique_id=params.ticket_unique_id,
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
    params = s.ChatSellEventParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/event_name.html",
            error_message="Form submitting error",
            room=room,
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

    assert room

    if not params.ticket_has_notes:
        c.save_message("Do you want to add notes?", "Without notes", room)
        log(log.ERROR, "Ticket without notes: [%s]", params.ticket_has_notes)
        return render_template(
            "chat/sell/ticket_document.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.ticket_notes:
        log(log.ERROR, "No ticket notes provided: [%s]", params.ticket_notes)
        return render_template(
            "chat/sell/11_ticket_notes.html",
            error_message="No ticket notes provided, please, add ticket notes or choose 'Without notes'",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    ticket = c.add_ticket_notes(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/12_ticket_document.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/get_ticket_document")
@login_required
def get_ticket_document():
    form: f.ChatTicketDocumentForm = f.ChatTicketDocumentForm()

    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == form.room_unique_id.data)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found: [%s]", form.room_unique_id.data)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error: [%s]",
            form.errors,
        )
        return render_template(
            "chat/sell/12_ticket_document.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            ticket_unique_id=form.ticket_unique_id.data,
        )

    error_message = c.add_ticket_document(form, room, current_user)

    if error_message:
        log(log.ERROR, "Not valid ticket document: [%s]", form.file.data)
        return render_template(
            "chat/sell/12_ticket_document.html",
            error_message=error_message,
            room=room,
            now=now_str,
            ticket_unique_id=form.ticket_unique_id.data,
        )

    return render_template(
        "chat/sell/13_name.html",
        room=room,
        now=now_str,
        ticket_unique_id=form.ticket_unique_id.data,
    )


@chat_sell_blueprint.route("/get_ticket_price")
@login_required
def get_ticket_price():
    params = s.ChatSellEventParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/event_name.html",
            error_message="Form submitting error",
            room=room,
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

    if not params.ticket_price:
        log(log.ERROR, "No ticket price provided: [%s]", params.ticket_notes)
        return render_template(
            "chat/sell/11_ticket_notes.html",
            error_message="No ticket ticket provided, please, add ticket price",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    assert room
    ticket = c.add_ticket_price(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/12_ticket_document.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_sell_blueprint.route("/event_form", methods=["GET", "POST"])
@login_required
def event_form():
    event_location = request.args.get("event_location")
    event_date = request.args.get("event_date")
    room_unique_id = request.args.get("room_unique_id")

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    error_message = ""
    if not event_location:
        log(log.ERROR, "No event location provided: [%s]", event_location)
        error_message += "No event location provided\n"
    if not event_date:
        log(log.ERROR, "No event date provided: [%s]", event_date)
        error_message += "No event date provided\n"

    if error_message:
        return render_template(
            "chat/sell/02_event_create.html",
            error_message=error_message,
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="No events found. Let's create a new one!",
    ).save(False)

    return render_template(
        "chat/sell/02_event_create.html",
        event_location=event_location,
        event_date=event_date,
        room=room,
        now=now_str,
        user=current_user,
    )


@chat_sell_blueprint.route("/create_event", methods=["GET", "POST"])
@login_required
def create_event():
    event_name = request.args.get("event_name")
    event_location = request.args.get("event_location")
    event_category = request.args.get("event_category")
    event_date = request.args.get("event_date")
    event_url = request.args.get("event_url")
    room_unique_id = request.args.get("room_unique_id")

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    error_message = ""

    if not event_name:
        log(log.ERROR, "No event name provided: [%s]", event_name)
        error_message += "No event name provided \n"
    if not event_location:
        log(log.ERROR, "No event location provided: [%s]", event_location)
        error_message += "No event location provided \n"
    if not event_category:
        log(log.ERROR, "No event category provided: [%s]", event_category)
        error_message += "No event category provided \n"
    if not event_date:
        log(log.ERROR, "No event date provided: [%s]", event_date)
        error_message += "No event date provided \n"
    if not event_url:
        log(log.ERROR, "No event url provided: [%s]", event_url)
        error_message += "No event url provided \n"

    if error_message:
        return render_template(
            "chat/sell/02_event_create.html",
            error_message=error_message,
            room=room,
            now=now_str,
            user=current_user,
        )

    # TODO: what should we do if there is no such location or category?
    location_query = m.Location.select().where(m.Location.name == event_location)
    location = db.session.scalar(location_query)
    if not location:
        log(log.ERROR, "Location not found: [%s]", event_location)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Location not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    category_query = m.Category.select().where(m.Category.name == event_category)
    category = db.session.scalar(category_query)
    if not category:
        log(log.ERROR, "Category not found: [%s]", event_category)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Category not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    if not event_date:
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Event date not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="There is no such events in our database. Let's create a new one!",
    ).save(False)
    m.Message(
        sender_id=current_user.id,
        room_id=room.id,
        text=f"{event_name}\n {event_location}\n {event_category}\n {event_date}\n {event_url}",
    ).save(False)

    event = m.Event(
        name=event_name,
        location=location,
        category=category,
        date_time=datetime.strptime(event_date, app.config["DATE_PICKER_FORMAT"]),
        url=event_url,
        creator_id=current_user.id,
    ).save()
    log(log.INFO, "Event created: [%s]", event)

    # TODO: check with Bard if events exist

    return render_template(
        "chat/sell/03_ticket_create.html",
        event=event,
        room=room,
        now=now_str,
        user=current_user,
    )


@chat_sell_blueprint.route("/ticket_form", methods=["GET", "POST"])
@login_required
def ticket_form():
    room_unique_id = request.args.get("room_unique_id")
    event_id = request.args.get("event_id")

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/03_ticket_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please, input ticket details.",
    ).save(False)

    # TODO: check with Bard if events exist
    event = db.session.scalar(m.Event.select().where(m.Event.unique_id == event_id))

    return render_template(
        "chat/sell/03_ticket_create.html",
        event=event,
        room=room,
        now=now_str,
        user=current_user,
    )


@chat_sell_blueprint.route("/create_ticket", methods=["GET", "POST"])
@login_required
def create_ticket():
    section = request.args.get("section")
    queue = request.args.get("queue")
    seat = request.args.get("seat")
    quantity = request.args.get("quantity")
    price = request.args.get("price")
    room_unique_id = request.args.get("room_unique_id")
    event_id = request.args.get("event_id")
    # TODO: add file input for ticket

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/03_ticket_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    error_message = ""

    if not section:
        log(log.ERROR, "No section provided: [%s]", section)
        error_message += "No section provided \n"
    if not queue:
        log(log.ERROR, "No queue provided: [%s]", queue)
        error_message += "No queue provided \n"
    if not seat:
        log(log.ERROR, "No seat provided: [%s]", seat)
        error_message += "No seat provided \n"
    if not quantity:
        log(log.ERROR, "No quantity provided: [%s]", quantity)
        error_message += "No quantity provided \n"
    if not price:
        log(log.ERROR, "No price provided: [%s]", price)
        error_message += "No price provided \n"

    event = db.session.scalar(m.Event.select().where(m.Event.unique_id == event_id))
    if not event:
        log(log.ERROR, "Event not found: [%s]", event_id)
        return render_template(
            "chat/sell/03_ticket_create.html",
            error_message="Event not found",
            event=event,
            room=room,
            now=now_str,
            user=current_user,
        )

    if error_message:
        return render_template(
            "chat/sell/03_ticket_create.html",
            error_message=error_message,
            event=event,
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="There is no such events in our database. Let's create a new one!",
    ).save(False)
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Event has been successfully added!",
    ).save(False)
    m.Message(
        sender_id=current_user.id,
        room_id=room.id,
        text=f"section: {section}\nqueue:{queue}\nseat:{seat}\nquantity:{quantity}\nprice:{price}",
    ).save(False)

    if price:
        price_gross = float(price) * app.config["PLATFORM_COMMISSION_RATE"]
        log(log.INFO, "Commission applied: [%s]", price_gross)

    ticket = m.Ticket(
        event=event,
        section=section,
        queue=queue,
        seat=seat,
        quantity=quantity,
        price_net=price,
        price_gross=price_gross,
        seller_id=current_user.id,
    ).save()

    return render_template(
        "chat/sell/04_ticket_success.html",
        ticket=ticket,
        room=room,
        now=now_str,
        user=current_user,
    )
