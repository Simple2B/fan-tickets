from datetime import datetime

from flask import current_app as app

from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db

from app.logger import log
from config import config

CFG = config()


def check_room_id(params: s.ChatSellParams) -> tuple[s.ChatSellResultParams, m.Room | None]:
    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == params.room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    # TODO: is needed to create a room if it does not exist?
    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return s.ChatSellResultParams(now_str=now_str, is_error=True), room

    if not params.room_unique_id:
        log(
            log.ERROR,
            "Form submitting error, room_unique_id: [%s]",
            params.room_unique_id,
        )
        return s.ChatSellResultParams(now_str=now_str, is_error=True), room

    return s.ChatSellResultParams(now_str=now_str), room


def send_message(bot_message: str, user_message: str, room: m.Room):
    """
    The function to save message for history in chat.
    It is save message from chat-bot and user.
    """
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=bot_message,
    ).save(False)
    m.Message(
        room_id=room.id,
        text=user_message,
    ).save()

    log(log.INFO, "Messages for history saved. Bot: [%s], user: [%s]", bot_message, user_message)


def create_event(params: s.ChatSellParams, room: m.Room) -> m.Event:
    location_query = m.Location.select().where(m.Location.name == params.event_location)
    location = db.session.scalar(location_query)

    if not location:
        log(log.INFO, "Location not found: [%s]", params.event_location)
        location = m.Location(name=params.event_location).save()

    category_query = m.Category.select().where(m.Category.name == params.event_category)
    category = db.session.scalar(category_query)

    if not category:
        log(log.INFO, "Event category not found: [%s]", params.event_category)
        category = m.Category(name=params.event_category).save()

    event_date = datetime.strptime(f"{params.event_date} {params.event_time}", app.config["DATE_CHAT_HISTORY_FORMAT"])
    event_query = m.Event.select().where(
        m.Event.name == params.event_name,
        m.Event.location == location,
        m.Event.category == category,
        m.Event.date_time == event_date,
    )
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found and was created a new one: [%s]", params.event_name)
        event = m.Event(
            name=params.event_name,
            location=location,
            category=category,
            date_time=event_date,
        ).save()

    send_message("Please, input event category", f"Event category: {params.event_category}", room)

    return event


def create_ticket(params: s.ChatSellParams, room: m.Room) -> m.Ticket | None:
    event = db.session.scalar(m.Event.select().where(m.Event.unique_id == params.event_unique_id))
    if not event:
        log(log.INFO, "Event not found: [%s]", params.event_unique_id)
        return None

    ticket = m.Ticket(
        m.Ticket.event == event,
        m.Ticket.ticket_type == params.ticket_type,
    ).save()

    send_message("Please, input ticket type", f"Ticket type: {params.ticket_type}", room)

    log(log.INFO, "Ticket created: [%s]", ticket.unique_id)
    return ticket


def add_ticket_category(params: s.ChatSellParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    assert params.ticket_category

    ticket.ticket_category = params.ticket_category
    ticket.save()
    log(log.INFO, "Ticket category added: [%s]", params.ticket_category)

    send_message("Please, input ticket category", f"Ticket category: {params.ticket_category}", room)

    return ticket


def add_ticket_section(params: s.ChatSellParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.section = params.ticket_section
    ticket.save()
    log(log.INFO, "Ticket section added: [%s]", params.ticket_section)

    send_message("Please, add ticket section", f"Ticket section: {params.ticket_section}", room)

    return ticket


def add_ticket_queue(params: s.ChatSellParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.queue = params.ticket_queue
    ticket.save()
    log(log.INFO, "Ticket queue added: [%s]", params.ticket_section)

    send_message("Please, add ticket queue", f"Ticket queue: {params.ticket_section}", room)

    return ticket


def add_ticket_seat(params: s.ChatSellParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.seat = params.ticket_seat
    ticket.save()
    log(log.INFO, "Ticket seat added: [%s]", params.ticket_section)

    send_message("Please, add ticket seat", f"Ticket seat: {params.ticket_section}", room)

    return ticket


def add_ticket_notes(params: s.ChatSellParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.description = params.ticket_notes
    ticket.save()
    log(log.INFO, "Ticket notes added: [%s]", params.ticket_notes)

    send_message("Please, input ticket notes", f"Ticket notes: {params.ticket_section}", room)

    return ticket


def add_ticket_document(form: f.ChatTicketDocumentForm, room: m.Room, user: m.User) -> str:
    response = c.image_upload(user, c.type_image.IDENTIFICATION)

    if 200 not in response:
        return "Not valid type of ticket document, please upload your ticket document with right format"

    send_message("Please upload your ticket document", "Ticket document has been uploaded", room)

    return ""


def add_ticket_price(params: s.ChatSellParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.description = params.ticket_notes
    ticket.save()
    log(log.INFO, "Ticket notes added: [%s]", params.ticket_notes)

    send_message("Please, input ticket notes", f"Ticket notes: {params.ticket_section}", room)

    return ticket
