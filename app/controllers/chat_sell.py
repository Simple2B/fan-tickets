import os
import re
from bardapi import Bard
from datetime import datetime, time, timedelta
from flask import current_app as app
from flask_login import current_user
import sqlalchemy as sa
from app.database import db
from app import controllers as c
from app import schema as s
from app import models as m

from app.logger import log
from config import config

CFG = config()


def get_event_by_name_bard(params: s.ChatSellEventParams, room) -> list[m.Event]:
    c.save_message(
        "Please, input official event name (matching the official website)",
        f"{params.user_message}",
        room,
    )
    # Firstly try to find event in database by exact match
    event_query = sa.select(m.Event).where(m.Event.name == params.user_message)
    event: m.Event = db.session.scalar(event_query)
    if event:
        return [event]

    # Secondly try to find event in database by partial match
    search_key_words = params.user_message.split(" ")
    events = []
    for word in search_key_words:
        event_query = sa.select(m.Event).where(m.Event.name.ilike(f"%{word}%"))
        events_search = db.session.scalars(event_query).all()
        events.extend(events_search)

    # If no events found in database, try to get event from Bard
    if not events:
        log(log.INFO, "Event not found in database: [%s]", params.user_message)

        try:
            # Establishing connection with Bard
            bard = Bard(token=os.environ.get("_BARD_API_KEY"))
        except Exception as e:
            log(log.ERROR, "Bard connection error: [%s]", e)
            return events

        question = f'Could you please tell me if there is an event with name "{params.user_message}" in Brasil and if yes give me a json with event details. For example:'

        json_example = """
            {
            "event_name": "official event name",
            "official_url": "https://someofficialurl.com",
            "location": "City name",
            "venue": "Sao Paolo Stadium",
            "date": "2024-02-24",
            "time": "20:00"
            }
        """

        message = f"{question}\n{json_example}"

        try:
            bard_response = bard.get_answer(message).get("content")
            log(log.INFO, "Bard response: [%s]", bard_response)
        except Exception as e:
            log(log.ERROR, "Bard get answer error: [%s]", e)
            return events

        if (
            "not able to help" in bard_response
            or "not able to assist" in bard_response
            or "unable to assist" in bard_response
            or "can't help you" in bard_response
            or "not programmed to assist with that" in bard_response
            or "nfortunately" in bard_response
        ):
            log(log.ERROR, "Bard response error: [%s]", bard_response)
            # Returning empty list if all three ways to find event failed
            return events

        # If Bard response is not an error, try to parse it
        try:
            json_str = re.search(r"```json\n(.*)\n```", bard_response, re.DOTALL).group(1)
            bard_response = s.BardResponse.model_validate_json(json_str)
            log(log.INFO, "Bard response json: [%s]", bard_response)
        except Exception as e:
            log(log.ERROR, "Bard response parse json error: [%s]", e)
            return events

        if bard_response.event_name:
            event_name = bard_response.event_name

        # Parsing date from Bard response
        try:
            match = re.search(r"\d{4}[-/]\d{2}[-/]\d{2}", bard_response.date)
            if match:
                first_date_str = match.group(0)
                first_date_str = first_date_str.replace("/", "-")
                event_date = datetime.strptime(first_date_str, CFG.BARD_DATE_FORMAT)
        except Exception as e:
            event_date_time = datetime.today() + timedelta(days=CFG.DAYS_TO_EVENT_MINIMUM)
            log(log.ERROR, "Date converting error: [%s]", e)
            log(log.ERROR, "Setting default date: [%s]", event_date_time)

        # Parsing time from Bard response
        try:
            match = re.search(r"\d{2}:\d{2}", bard_response.time)
            if match:
                event_time_str = match.group(0)
                hours = int(event_time_str[:2])
                minutes = int(event_time_str[3:])
                event_date_time = event_date.replace(hour=hours, minute=minutes)
        except Exception as e:
            event_date_time = event_date_time.replace(
                hour=CFG.DEFAULT_EVENT_TIME_HOURS,
                minute=CFG.DEFAULT_EVENT_TIME_MINUTES,
            )
            log(log.ERROR, "Time converting error: [%s]", e)
            log(log.ERROR, "Setting default time: [%s]", event_date_time)

        # Parsing location from Bard response
        location_id = None
        if bard_response.location:
            location_query = sa.select(m.Location).where(m.Location.name == bard_response.location)
            location = db.session.scalar(location_query)
            if not location:
                location = m.Location(name=bard_response.location).save()
            location_id = location.id

        # Getting the category by unique id
        category_query = sa.select(m.Category).where(m.Category.name == params.event_category_id)
        category: m.Category = db.session.scalar(category_query)

        # Creating a new event in database if we have at least minimal data
        event = m.Event(
            name=event_name,
            url=bard_response.official_url,
            location_id=location_id,
            category_id=category.id,
            venue=bard_response.venue,
            date_time=event_date_time,
            creator_id=current_user.id,
        ).save()
        events.append(event)
        log(log.INFO, "User [%s] has created a new event: [%s]", current_user, event)

    return events


def create_event(params: s.ChatSellEventParams, room: m.Room, user: m.User) -> m.Event:
    category_query = sa.select(m.Category).where(m.Category.unique_id == params.event_category_id)
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


def create_ticket(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket:
    event = db.session.scalar(sa.select(m.Event).where(m.Event.unique_id == params.event_unique_id))
    ticket = m.Ticket(
        event=event,
        ticket_type=params.ticket_type,
        seller_id=current_user.id,
        is_deleted=True,
    ).save(False)

    c.save_message(
        "Got it! How many tickets do you want to sell?",
        params.tickets_quantity_answer,
        room,
    )

    log(log.INFO, "Ticket created: [%s]", ticket.unique_id)
    return ticket


def create_paired_ticket(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    first_ticket_query = sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id)
    first_ticket: m.Ticket = db.session.scalar(first_ticket_query)

    first_ticket.is_paired = True

    second_ticket = m.Ticket(
        event=first_ticket.event,
        ticket_type=first_ticket.ticket_type,
        ticket_category=first_ticket.ticket_category,
        seller_id=current_user.id,
        is_paired=True,
        pair_unique_id=first_ticket.unique_id,
    )
    db.session.add(second_ticket)
    db.session.flush()
    first_ticket.pair_unique_id = second_ticket.unique_id
    db.session.commit()

    log(log.INFO, "Paired tickets created: [%s], [%s]", first_ticket.unique_id, second_ticket.unique_id)

    return first_ticket


def add_ticket_category(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.ticket_category = params.ticket_category.replace(" ", "_").lower()
    ticket.save(False)

    c.save_message("Please, add ticket category", f"Ticket category: {params.ticket_category}", room)

    log(log.INFO, "Ticket category added: [%s]", params.ticket_category)
    return ticket


def add_ticket_section(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket | None:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.section = params.user_message
    ticket.save()

    c.save_message("Please, add ticket section", f"Ticket section: {params.user_message}", room)

    log(log.INFO, "Ticket section added: [%s]", params.ticket_section)
    return ticket


def add_ticket_queue(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    ticket.queue = params.user_message
    ticket.save()

    c.save_message("Please, add ticket queue", f"Ticket queue: {params.user_message}", room)

    log(log.INFO, "Ticket queue added: [%s]", ticket.queue)
    return ticket


def add_ticket_seat(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    if ticket.is_paired and "," in params.user_message:
        seat1, seat2 = params.user_message.split(",")
        seat1 = seat1.strip()
        seat2 = seat2.strip()
        ticket.seat = seat1
        ticket.save(False)
        ticket2_query = sa.select(m.Ticket).where(m.Ticket.pair_unique_id == ticket.unique_id)
        ticket2: m.Ticket = db.session.scalar(ticket2_query)
        ticket2.seat = seat2
        ticket2.save()
        log(log.INFO, "Paired tickets seat added: [%s], [%s]", ticket.seat, ticket2.seat)
        c.save_message(
            "Please enter seats for both tickets separating them with comma. For example: 23,24",
            f"Tickets' seats: {ticket.seat}, {ticket2.seat}",
            room,
        )
    else:
        ticket.seat = params.user_message
        ticket.save()
        log(log.INFO, "Ticket seat added: [%s]", ticket.seat)
        c.save_message("Please, add ticket seat", f"Ticket seat: {ticket.seat}", room)

    return ticket


def add_ticket_notes(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    ticket.description = params.user_message
    ticket.save()
    log(log.INFO, "Ticket notes added: [%s]", ticket.description)

    c.save_message("Please, input ticket notes", f"Ticket notes: {ticket.description}", room)

    return ticket


def check_paired_ticket_fields(ticket: m.Ticket) -> None:
    if not ticket.is_paired:
        return

    ticket2_query = sa.select(m.Ticket).where(m.Ticket.unique_id == ticket.pair_unique_id)
    ticket2: m.Ticket = db.session.scalar(ticket2_query)
    if not ticket.section and ticket2.section:
        ticket.section = ticket2.section
        log(log.INFO, "Paired ticket section added: [%s]", ticket.section)
    if not ticket.queue and ticket2.queue:
        ticket.queue = ticket2.queue
        log(log.INFO, "Paired ticket queue added: [%s]", ticket.queue)
    if not ticket.seat and ticket2.seat:
        ticket.seat = ticket2.seat
        log(log.INFO, "Paired ticket seat added: [%s]", ticket.seat)
    if not ticket.description and ticket2.description:
        ticket.description = ticket2.description
        log(log.INFO, "Paired ticket notes added: [%s]", ticket.description)
    if not ticket.price_net and ticket2.price_net:
        ticket.price_net = ticket2.price_net
        log(log.INFO, "Paired ticket price_net added: [%s]", ticket.price_net)
    if not ticket.price_gross and ticket2.price_gross:
        ticket.price_gross = ticket2.price_gross
        log(log.INFO, "Paired ticket price_gross added: [%s]", ticket.price_gross)
    ticket.save()

    return


def add_ticket_wallet_id(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket:
    ticket_query = sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    if ticket.is_paired:
        ticket2_query = m.Ticket.select().where(m.Ticket.unique_id == ticket.pair_unique_id)
        ticket2: m.Ticket = db.session.scalar(ticket2_query)

        if not ticket.wallet_id:
            ticket.wallet_id = params.user_message
            check_paired_ticket_fields(ticket)
            ticket.is_deleted = False
            ticket.save()
            log(log.INFO, "Ticket wallet id added: [%s]", ticket.wallet_id)
            c.save_message("Please, input ticket wallet id", f"Ticket wallet_id: {ticket.wallet_id}", room)

            if ticket.wallet_id and ticket2.wallet_id:
                is_second_wallet_id_input = False
            else:
                is_second_wallet_id_input = True
            return ticket, is_second_wallet_id_input

        elif not ticket2.wallet_id:
            ticket2.wallet_id = params.user_message
            check_paired_ticket_fields(ticket2)
            ticket2.is_deleted = False
            ticket2.save()
            log(log.INFO, "Second ticket wallet id added: [%s]", ticket.wallet_id)
            c.save_message("Please, input second ticket wallet id", f"Ticket wallet_id: {ticket.wallet_id}", room)

    else:
        ticket.wallet_id = params.user_message
        ticket.is_deleted = False
        ticket.save()
        log(log.INFO, "Ticket wallet id added: [%s]", ticket.wallet_id)
        c.save_message("Please, input ticket wallet id", f"Ticket wallet_id: {ticket.wallet_id}", room)

    return ticket, False


def add_ticket_document(
    params: s.ChatSellTicketParams,
    files,
    ticket: m.Ticket,
    room: m.Room,
) -> m.Ticket | None:
    if not ticket or not files:
        log(log.INFO, "Ticket not found: [%s]", params.ticket_unique_id)
        return None

    ticket.file = files[0].read()
    check_paired_ticket_fields(ticket)
    ticket.is_deleted = False
    ticket.save()

    c.save_message("Please, input ticket PDF document", f"Ticket document: {files[0].filename}", room)
    log(log.INFO, "Ticket document added: [%s]", files[0].filename)

    if len(files) > 1:
        ticket2_query = sa.select(m.Ticket).where(m.Ticket.unique_id == ticket.pair_unique_id)
        ticket2: m.Ticket = db.session.scalar(ticket2_query)
        ticket2.file = files[1].read()
        check_paired_ticket_fields(ticket2)
        ticket2.is_deleted = False
        ticket2.save()
        log(log.INFO, "Paired ticket document added: [%s]", files[1].filename)

    return ticket


def add_ticket_price(params: s.ChatSellTicketParams, room: m.Room, price: int) -> m.Ticket:
    ticket: m.Ticket = db.session.scalar(sa.select(m.Ticket).where(m.Ticket.unique_id == params.ticket_unique_id))
    price_gross = int(round(price * app.config["PLATFORM_COMMISSION_RATE"]))
    if not ticket.is_paired:
        ticket.price_net = price
        ticket.price_gross = price_gross
        c.save_message("Please, input ticket price", f"Ticket price: {price_gross}", room)
    else:
        ticket.price_net = int(round(price / 2))
        ticket.price_gross = int(round(ticket.price_net * app.config["PLATFORM_COMMISSION_RATE"]))
        c.save_message("Please, input the price for two tickets", f"Ticket price: {price_gross}", room)

    ticket.save()
    log(log.INFO, "Ticket price added: [%s], price_gross: [%s]", params.ticket_notes, price_gross)

    return ticket
