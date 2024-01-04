import sqlalchemy as sa

from flask import current_app as app

from app import controllers as c
from app import schema as s
from app import models as m
from app.database import db

from app.logger import log


def get_events_by_event_name(event_name: str, room: m.Room) -> list[m.Event]:
    event_query = sa.select(m.Event).where(m.Event.name.ilike(f"%{event_name}%"))
    events = db.session.scalars(event_query).all()
    if not events:
        log(log.INFO, "Events not found: [%s]", event_name)
        c.save_message(
            "Great! To get started, could you please write below name of the event you're looking for?",
            f"{event_name}",
            room,
        )
    return events


def get_events_by_location_event_name(params: s.ChatBuyEventParams, room: m.Room) -> list[m.Event] | None:
    location_query = sa.select(m.Location).where(m.Location.unique_id == params.location_unique_id)
    location = db.session.scalar(location_query)

    if not location:
        log(log.INFO, "Location not found: [%s]", params.location_unique_id)
        return None

    event_query = sa.select(m.Event).where(m.Event.name == params.event_name, m.Event.location_id == location.id)
    events = db.session.scalars(event_query).all()

    if not events:
        log(log.INFO, "Events not found: [%s], [%s]", params.event_name, location.name)
        c.save_message(
            "Great! To get started, could you please write below name of the event you're looking for?",
            f"{params.event_name}",
            room,
        )

    c.save_message(
        "Fantastic choice! There are several location for this event. Please choose below👇",
        f"{location.name}",
        room,
    )
    return events


def get_tickets_by_event(event: m.Event, room: m.Room) -> list[m.Ticket] | None:
    tickets_query = sa.select(m.Ticket).where(
        m.Ticket.event_id == event.id,
        m.Ticket.is_reserved.is_(False),
        m.Ticket.is_sold.is_(False),
    )
    tickets = db.session.scalars(tickets_query).all()

    if not tickets:
        log(log.INFO, "Tickets not found: [%s]", event.name)
        c.save_message(
            "Great! To get started, could you please write below name of the event you're looking for?",
            f"{event.name}",
            room,
        )
    return tickets


def get_tickets_by_event_id(event_unique_id: str, room: m.Room) -> list[m.Ticket] | None:
    event_query = sa.select(m.Event).where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", event_unique_id)
        return None

    tickets_query = sa.select(m.Ticket).where(
        m.Ticket.event_id == event.id,
        m.Ticket.is_reserved.is_(False),
        m.Ticket.is_sold.is_(False),
    )
    tickets = db.session.scalars(tickets_query).all()

    if not tickets:
        log(log.INFO, "Tickets not found: [%s]", event_unique_id)

    c.save_message(
        f"Great news! We have found {len(tickets)} available tickets",
        "All tickets",
        room,
    )

    return tickets


def get_cheapest_tickets(
    tickets: list[m.Ticket],
    room: m.Room,
    limit_ticket: bool,
    add_ticket: bool,
) -> list[m.Ticket]:
    tickets.sort(key=lambda ticket: ticket.price_gross)
    event_name = tickets[0].event.name

    if not limit_ticket:
        tickets = tickets[: app.config["TICKETS_PER_CHAT"]]

    if add_ticket:
        c.save_message(
            "Got it! Do you want to buy another one or proceed to purchase?",
            "Add ticket",
            room,
        )
    else:
        c.save_message(
            "Great! To get started, could you please write below name of the event you're looking for?",
            f"{event_name}",
            room,
        )

    return tickets


def book_ticket(ticket_unique_id: str, user: m.User, room: m.Room) -> m.Ticket | None:
    ticket_query = sa.select(m.Ticket).where(m.Ticket.unique_id == ticket_unique_id)
    ticket = db.session.scalar(ticket_query)

    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", ticket_unique_id)
        return None

    ticket.is_reserved = True
    ticket.buyer_id = user.id

    # TODO: create string with ticket info
    c.save_message("We have found tickets. What ticket do you want?", f"ticket seat: {ticket.seat}", room)

    return ticket


def calculate_total_price(user: m.User) -> s.ChatBuyTicketTotalPrice | None:
    tickets_query = sa.select(m.Ticket).where(
        m.Ticket.buyer_id == user.id,
        m.Ticket.is_reserved.is_(True),
        m.Ticket.is_sold.is_(False),
    )
    tickets = db.session.scalars(tickets_query).all()

    if not tickets:
        log(log.INFO, "Tickets not found: [%s]", user.id)
        return None

    price_total = 0
    price_service = 0
    price_net = 0
    for ticket in tickets:
        ticket_price_gross = ticket.price_net * app.config["PLATFORM_COMMISSION_RATE"]
        ticket.price_gross = ticket_price_gross

        price_total += ticket_price_gross
        price_service += ticket_price_gross - ticket.price_net
        price_net += ticket.price_net

    # TODO: Do we need to round the total price here?
    return s.ChatBuyTicketTotalPrice(
        service=round(price_service, 2),
        total=round(price_total, 2),
        net=round(price_net, 2),
    )


def get_locations_by_events(events: list[m.Event], room: m.Room) -> list[m.Location] | None:
    events_names = [event.name for event in events]
    locations_query = sa.select(m.Location).filter(m.Location.event.has(m.Event.name.in_(events_names)))
    locations = db.session.scalars(locations_query).all()

    if not locations:
        log(log.INFO, "Locations not found: [%s]", events)
        c.save_message(
            "Great! To get started, could you please write below name of the event you're looking for?",
            f"{events[0].name}",
            room,
        )
    return locations


def subscribe_event(event_unique_id: str, user: m.User):
    event_query = sa.select(m.Event).where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", event_unique_id)

    user.subscribed_events.append(event)


def create_user(email: str) -> m.User:
    user = m.User(
        email=email,
    )
    return user
