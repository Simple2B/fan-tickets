import os
import re
from bardapi import Bard
from datetime import datetime, time
from flask import current_app as app
import sqlalchemy as sa
from app.database import db
from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m

from app.logger import log
from config import config

CFG = config()


def get_event_by_name_bard(event_name: str) -> list[m.Event]:
    event_query = sa.select(m.Event).where(m.Event.name.ilike(event_name))
    events = db.session.scalars(event_query).all()
    if not events:
        log(log.INFO, "Event not found in database: [%s]", event_name)

        try:
            bard = Bard(token=os.environ.get("_BARD_API_KEY"))

            question = f'Could you please tell me if there is an event with name "{event_name}" and if yes give me a json with event details. For example:'

            json_example = """
                {
                "event_name": "official event name",
                "official_url": "https://someoficcialurl.com",
                "location": "Sao Paolo",
                "venue": "Sao Paolo Stadium",
                "date": "2024/01/01",
                "time": "20:00"
                }
            """

            message = f"{question}\n{json_example}"

            bard_response = bard.get_answer(message).get("content")
            if "not able to help" in bard_response or "not able to assist" in bard_response:
                return s.EventValidation(events=events, bard_response=bard_response)
            # bard_response = 'Yes, there is actually an event named "Afterlife São Paulo 2024" taking place! Here are the details in JSON format:\n\n```json\n{\n  "event_name": "Afterlife São Paulo 2024",\n  "official_url": "https://jp.ra.co/events/1819014",\n  "location": "São Paulo, Brazil",\n  "venue": "Autódromo de Interlagos (TBA)",\n  "date": "2024-02-24",\n  "time": "16:00 - 23:59"\n}\n```\n\nPlease note that the specific location within the Autódromo de Interlagos is still to be announced (TBA).\n\nHere are some additional details about the event you might find helpful:\n\n* This is a music festival focused on electronic music, hosted by the Afterlife record label.\n* The headliners are Tale Of Us, with supporting sets from Omnya, Binaryh, ANNA, MRAK, Cassian B2B Kevin de Vries, Anyma, and more.\n* Tickets are available for purchase through Live Nation and Ticketmaster Brasil.\n\nI hope this information is helpful! Enjoy the event!\n'
            json_str = re.search(r"```json\n(.*)\n```", bard_response, re.DOTALL).group(1)
            bard_response = s.BardResponse.model_validate_json(json_str)

            event = m.Event(
                name=bard_response.event_name,
                url=bard_response.official_url,
                location=m.Location(name=bard_response.location),
                venue=bard_response.venue,
                date_time=datetime.strptime(bard_response.date_time, CFG.DATE_PICKER_FORMAT),
            ).save()
            events.append(event)
        except Exception as e:
            log(log.ERROR, "Bard error: [%s]", e)

    return events


def create_event(params: s.ChatSellEventParams, room: m.Room, user: m.User) -> m.Event:
    category_query = sa.select(m.Category).where(m.Category.name == params.event_category_id)
    category = db.session.scalar(category_query)

    if not category:
        log(log.INFO, "Event category not found: [%s]", params.event_category_id)
        category = m.Category(name=params.event_category_id).save(False)

    event = m.Event(
        name=params.event_name,
        category=category,
        creator_id=user.id,
        url=params.user_message,
    ).save()

    log(log.INFO, "Event created: [%s]", event)
    return event


def add_event_location(params: s.ChatSellEventParams) -> bool:
    event_query = sa.select(m.Event).where(m.Event.unique_id == params.event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", params.event_unique_id)
        return False

    location_query = sa.select(m.Location).where(m.Location.name == params.user_message)
    location = db.session.scalar(location_query)

    if not location:
        location = m.Location(name=params.user_message).save(False)

    event.location = location
    event.save()

    return True


def add_event_venue(params: s.ChatSellEventParams) -> bool:
    event_query = sa.select(m.Event).where(m.Event.unique_id == params.event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", params.event_unique_id)
        return False

    event.venue = params.user_message
    event.save()

    return True


def add_event_date(params: s.ChatSellEventParams, event_date: datetime) -> bool:
    event_query = sa.select(m.Event).where(m.Event.unique_id == params.event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", params.event_unique_id)
        return False

    event.date_time = event_date
    event.save()

    return True


def add_event_time(params: s.ChatSellEventParams, event_time: time) -> bool:
    event_query = sa.select(m.Event).where(m.Event.unique_id == params.event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", params.event_unique_id)
        return False

    event.date_time = event.date_time.replace(hour=event_time.hour, minute=event_time.minute)
    event.save()

    return True


def create_ticket(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    event = db.session.scalar(sa.select(m.Event).where(m.Event.unique_id == params.event_unique_id))
    if not event:
        log(log.INFO, "Event not found: [%s]", params.event_unique_id)
        return None

    ticket = m.Ticket(
        m.Ticket.event == event,
        m.Ticket.ticket_type == params.ticket_type,
    ).save(False)

    c.save_message("Please, add ticket type", f"Ticket type: {params.ticket_type}", room)

    log(log.INFO, "Ticket created: [%s]", ticket.unique_id)
    return ticket


def add_ticket_category(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.ticket_category = params.ticket_category
    ticket.save(False)

    c.save_message("Please, add ticket category", f"Ticket category: {params.ticket_category}", room)

    log(log.INFO, "Ticket category added: [%s]", params.ticket_category)
    return ticket


def add_ticket_section(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.section = params.ticket_section
    ticket.save(False)

    c.save_message("Please, add ticket section", f"Ticket section: {params.ticket_section}", room)

    log(log.INFO, "Ticket section added: [%s]", params.ticket_section)
    return ticket


def add_ticket_queue(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.queue = params.ticket_queue
    ticket.save(False)

    c.save_message("Please, add ticket queue", f"Ticket queue: {params.ticket_section}", room)

    log(log.INFO, "Ticket queue added: [%s]", params.ticket_section)
    return ticket


def add_ticket_seat(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.seat = params.ticket_seat
    ticket.save(False)
    log(log.INFO, "Ticket seat added: [%s]", params.ticket_section)

    c.save_message("Please, add ticket seat", f"Ticket seat: {params.ticket_section}", room)

    return ticket


def add_ticket_notes(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.description = params.ticket_notes
    ticket.save(False)
    log(log.INFO, "Ticket notes added: [%s]", params.ticket_notes)

    c.save_message("Please, input ticket notes", f"Ticket notes: {params.ticket_section}", room)

    return ticket


def add_ticket_document(form: f.ChatTicketDocumentForm, room: m.Room, user: m.User) -> str:
    response = c.image_upload(user, c.ImageType.IDENTIFICATION)

    if 200 not in response:
        return "Not valid type of ticket document, please upload your ticket document with right format"

    c.save_message("Please upload your ticket document", "Ticket document has been uploaded", room)

    return ""


def add_ticket_price(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    assert params.ticket_price
    price_gross = float(params.ticket_price) * app.config["PLATFORM_COMMISSION_RATE"]
    ticket.price_net = params.ticket_price
    ticket.price_gross = price_gross
    ticket.save()
    log(log.INFO, "Ticket price added: [%s], price_gross: [%s]", params.ticket_notes, price_gross)

    c.save_message("Please, input ticket price", f"Ticket price: {params.ticket_section}", room)

    return ticket