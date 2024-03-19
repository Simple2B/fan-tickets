import re
import os
import json
import requests
from datetime import datetime, timedelta, time
from flask_login import current_user
from werkzeug.datastructures.file_storage import FileStorage
import sqlalchemy as sa
from app.database import db
from app import controllers as c
from app import schema as s
from app import models as m

from app.logger import log
from config import config

CFG = config()

API_KEY = os.environ.get("BARD_API_KEY")
BARD_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"


def ask_bard_for_event(event_name: str) -> tuple[str, bool]:
    question = f'Could you please tell me if there is an event in Brasil that has name similar to "{event_name}" and if yes give me a json with event details. For example:'
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
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": message},
                ],
            }
        ]
    }
    bard_response = requests.post(BARD_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        response_text = bard_response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        log(log.ERROR, "Bard response error: [%s]", e)
        return bard_response.text, False

    return response_text, True


def parse_date_with_bard(date_str: str) -> str:
    message = f"Could you please reformat this date: {date_str} in format YYYY-MM-DD? For example: 2023-12-31. If there is a range of dates, please give me the first one."
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": message},
                ],
            }
        ]
    }
    bard_response = requests.post(BARD_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        response_date_str = bard_response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        log(log.ERROR, "Bard response error: [%s]", e)
        default_date_str = datetime.today() + timedelta(days=CFG.DAYS_TO_EVENT_MINIMUM)
        return default_date_str.strftime(CFG.BARD_DATE_FORMAT)

    return response_date_str


def parse_time_with_bard(time_str: str) -> str:
    message = f"Could you please reformat this time: {time_str} in format HH:MM? For example: 20:00. If there is a range of times, please give me the first one."
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": message},
                ],
            }
        ]
    }
    bard_response = requests.post(BARD_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        response_time_str = bard_response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        log(log.ERROR, "Bard response error: [%s]", e)
        response_time_str = "20:00"

    return response_time_str


def parse_bard_response(bard_response: str) -> tuple[s.BardResponse | str, bool]:
    """
    Bard response examples:
    '{\n "event_name": "Rock in Rio 2024",\n "official_url": "https://rockinrio.com/",\n "location": "Rio de Janeiro",\n "venue": "Cidade do Rock",\n "date": "2024-09-27",\n "time": "18:00"\n}'
    '{\n  "event_name": "Lollapalooza Brasil",\n  "official_url": "https://www.lollapaloozabr.com/",\n  "location": "São Paulo",\n  "venue": "Autódromo de Interlagos",\n  "date": "2023-03-24",\n  "time": "13:00"\n}'
    'Yes, there is an event in Brazil with a name similar to "Warung day festival".\n\n```\n{\n  "event_name": "Warung Beach Club Day Festival",\n  "official_url": "https://www.warungbeachclub.com.br/eventos/",\n  "location": "Praia de Jurerê Internacional, Florianópolis, Santa Catarina",\n  "venue": "Warung Beach Club",\n  "date": "2023-01-01",\n  "time": "12:00"\n}\n```'
    'Yes, there is an event in Brazil with a name similar to "Turnstile Latin America 2024". It is called "Turnstile Latin America 2023". Here are the details of the event:\n\n```\n{\n  "event_name": "Turnstile Latin America 2023",\n  "official_url": "https://www.turnstilelatinamerica.com/",\n  "location": "São Paulo, Brazil",\n  "venue": "São Paulo Expo",\n  "date": "2023-05-23",\n  "time": "10:00 AM - 6:00 PM"\n}\n```'
    'Yes, there is an event in Brazil that has a name similar to "Metallica". Here are the details:\n\n```\n{\n  "event_name": "Metallica: WorldWired Tour 2023",\n  "official_url": "https://www.metallica.com/tour/",\n  "location": "São Paulo, Brazil",\n  "venue": "Estádio do Morumbi",\n  "date": "2023-05-12",\n  "time": "20:00"\n}\n```'
    '{\n  "event_name": "Brunch Electronik São Paulo",\n  "official_url": "https://brunchelectronik.com.br/sao-paulo/",\n  "location": "São Paulo, Brazil",\n  "venue": "São Paulo Expo",\n  "date": "2023-12-02",\n  "time": "12:00 - 22:00"\n}'
    '{\n  "event_name": "Rock in Rio",\n  "official_url": "https://rockinrio.com/",\n  "location": "Rio de Janeiro",\n  "venue": "Cidade do Rock",\n  "date": "September 2-11, 2022",\n  "time": "Starting at 7 pm"\n}'
    """
    try:
        parsed_response = s.BardResponse.model_validate_json(bard_response)
    except Exception as e:
        log(log.ERROR, "Bard response parse json error: [%s]", e)
        return bard_response, False

    if parsed_response.date and not re.match(r"\d{4}[-/]\d{2}[-/]\d{2}", parsed_response.date):
        log(log.ERROR, "Asking Bard to parse stringified date: [%s]", parsed_response.date)
        parsed_response.date = parse_date_with_bard(parsed_response.date)

    if parsed_response.time and not re.match(r"\d{2}:\d{2}", parsed_response.time):
        log(log.ERROR, "Asking Bard to parse stringified time: [%s]", parsed_response.time)
        parsed_response.time = parse_time_with_bard(parsed_response.time)

    return parsed_response, True


def create_event_date_time(date: str, time: str) -> datetime:
    if not date and not time:
        return datetime.now() + timedelta(days=CFG.DAYS_TO_EVENT_MINIMUM)

    date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    return date_time


def get_event_by_name_bard(params: s.ChatSellEventParams | s.ChatBuyEventParams, room, from_buy=False) -> list[m.Event]:
    assert params.user_message

    if not from_buy:
        c.save_message(
            "Please, input official event name (matching the official website)",
            f"{params.user_message}",
            room,
        )
    # Firstly try to find event in database by exact match
    event_query = sa.select(m.Event).where(
        m.Event.name.ilike(f"%{params.user_message}%"), m.Event.date_time >= datetime.now()
    )
    events = db.session.scalars(event_query).all()
    if events:
        return events

    # Secondly try to find event in database by partial match
    search_key_words = params.user_message.split(" ") if params.user_message else []
    events = []
    for word in search_key_words:
        event_query = sa.select(m.Event).where(m.Event.name.ilike(f"%{word}%"), m.Event.date_time >= datetime.now())
        events_search = db.session.scalars(event_query).all()
        events.extend(events_search)

    # If no events found in database, try to get event from Bard
    if not events:
        log(log.INFO, "Event not found in database: [%s]", params.user_message)

        bard_event_check, event_found = ask_bard_for_event(params.user_message)
        if not event_found:
            log(log.INFO, "Event is not found by Bard: [%s]", bard_event_check)
            return events

        event_data, parsed_successfully = parse_bard_response(bard_event_check)
        if not parsed_successfully:
            log(log.ERROR, "Bard response error: [%s]", event_data)
            return events

        assert isinstance(event_data, s.BardResponse)

        # Getting the location
        location_query = sa.select(m.Location).where(m.Location.name == event_data.location)
        location: m.Location = db.session.scalar(location_query)
        if not location:
            log(log.INFO, "Location not found: [%s]. Creating new location in db.", event_data.location)
            location = m.Location(name=event_data.location).save()

        category_query = sa.select(m.Category).where(m.Category.name == "Shows")
        category: m.Category = db.session.scalar(category_query)

        event_date_time = create_event_date_time(event_data.date, event_data.time)

        # Creating a new event in database if we have at least minimal data
        event = m.Event(
            name=event_data.event_name,
            url=event_data.official_url,
            location_id=location.id,
            category_id=category.id,
            venue=event_data.venue,
            date_time=event_date_time,
            creator_id=current_user.id,
        ).save()
        events.append(event)
        log(log.INFO, "User [%s] has created a new event: [%s]", current_user, event)

    return events


def get_event_by_uuid(event_unique_id: str, room) -> m.Event:
    event_query = sa.select(m.Event).where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)
    if not event:
        log(log.INFO, "Event not found: [%s]", event_unique_id)
        raise ValueError(f"Event not found: {event_unique_id}")

    c.save_message("Super! Please check if this event is right?", event.name, room)
    return event


def create_event(params: s.ChatSellEventParams, room: m.Room, user: m.User) -> m.Event:
    category_query = sa.select(m.Category).where(m.Category.unique_id == params.event_category_id)
    category = db.session.scalar(category_query)

    if not category:
        log(log.INFO, "Event category not found: [%s]", params.event_category_id)
        category = m.Category(name=params.event_category_id).save(False)

    event = m.Event(
        date_time=datetime.now(),
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

    try:
        event.date_time = event.date_time.replace(hour=event_time.hour, minute=event_time.minute)
        event.save()
    except Exception as e:
        log(log.ERROR, "Event time adding error: [%s]", e)
        return False

    return True


def create_ticket(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket:
    event = db.session.scalar(sa.select(m.Event).where(m.Event.unique_id == params.event_unique_id))
    ticket = m.Ticket(
        event=event,
        ticket_type=params.ticket_type,
        seller_id=current_user.id,
        is_deleted=True,
    ).save(False)

    tickets_quantity_answer = params.tickets_quantity_answer if params.tickets_quantity_answer else "1"
    c.save_message(
        "Got it! How many tickets do you want to sell?",
        tickets_quantity_answer,
        room,
    )

    log(log.INFO, "Ticket created: [%s]", ticket.unique_id)
    return ticket


def create_paired_ticket(params: s.ChatSellTicketParams, room: m.Room) -> m.Ticket:
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

    if params.ticket_category:
        ticket.ticket_category = params.ticket_category.replace(" ", "_").lower()
    ticket.save()

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
    if ticket.is_paired and params.user_message and "," in params.user_message:
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


def add_ticket_wallet_id(params: s.ChatSellTicketParams, room: m.Room) -> tuple[m.Ticket, bool]:
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


def check_file_type(files: list[FileStorage]) -> bool:
    for file in files:
        if not isinstance(file, FileStorage):
            return False
        if file.mimetype != "application/pdf":
            return False
    return True


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

    global_fee_settings = db.session.scalar(sa.select(m.GlobalFeeSettings))
    total_commission = 1 + (global_fee_settings.service_fee + global_fee_settings.bank_fee) / 100

    price_gross = int(round(price * total_commission))
    if not ticket.is_paired:
        ticket.price_net = price
        ticket.price_gross = price_gross
        c.save_message("Please, input ticket price", f"Ticket price: {price_gross}", room)
    else:
        ticket.price_net = int(round(price / 2))
        ticket.price_gross = int(round(ticket.price_net * total_commission))
        c.save_message("Please, input the price for two tickets", f"Ticket price: {price_gross}", room)

    ticket.save()
    log(log.INFO, "Ticket price added: [%s], price_gross: [%s]", params.ticket_notes, price_gross)

    return ticket
