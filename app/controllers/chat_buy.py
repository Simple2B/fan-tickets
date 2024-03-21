from datetime import datetime, UTC
import sqlalchemy as sa

from flask import current_app as app

from app import controllers as c
from app import schema as s
from app import models as m
from app.database import db
from app.logger import log


def get_events_by_event_name(event_name: str, room: m.Room) -> list[m.Event]:
    event_query = sa.select(m.Event).where(m.Event.name.ilike(f"%{event_name}%"), m.Event.date_time >= datetime.now())
    events = db.session.scalars(event_query).all()
    if not events:
        log(log.INFO, "Events not found: [%s]", event_name)
    return events


def get_events_by_location_event_name(params: s.ChatBuyEventParams, room: m.Room) -> list[m.Event] | None:
    location_query = sa.select(m.Location).where(m.Location.unique_id == params.location_unique_id)
    location = db.session.scalar(location_query)

    if not location:
        log(log.INFO, "Location not found: [%s]", params.location_unique_id)
        return None

    event_query = sa.select(m.Event).where(
        m.Event.name == params.event_name,
        m.Event.location_id == location.id,
        m.Event.date_time >= datetime.now(),
    )
    events = db.session.scalars(event_query).all()

    if not events:
        log(log.INFO, "Events not found: [%s], [%s]", params.event_name, location.name)

    c.save_message(
        "Fantastic choice! There are several location for this event. Please choose below👇",
        f"Location:{location.name}, Event:{params.event_name}",
        room,
    )
    return events


def get_tickets_by_event(event: m.Event, room: m.Room) -> list[m.Ticket] | None:
    tickets_query = sa.select(m.Ticket).where(
        m.Ticket.event_id == event.id,
        m.Ticket.is_deleted.is_(False),
    )
    tickets = db.session.scalars(tickets_query).all()

    tickets_available = [ticket for ticket in tickets if ticket.is_available]

    if not tickets_available:
        log(log.INFO, "Tickets not found: [%s]", event.name)

    return tickets_available


def get_tickets_by_event_id(params: s.ChatBuyTicketParams, room: m.Room) -> list[m.Ticket] | None:
    event_query = sa.select(m.Event).where(m.Event.unique_id == params.event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", params.event_unique_id)
        return None

    tickets_query = sa.select(m.Ticket).where(
        m.Ticket.event_id == event.id,
        m.Ticket.is_deleted.is_(False),
    )
    tickets = db.session.scalars(tickets_query).all()

    if not tickets:
        log(log.INFO, "Tickets not found: [%s]", params.event_unique_id)

    tickets_available = [ticket for ticket in tickets if ticket.is_available]

    return tickets_available


def get_sorted_tickets(
    tickets: list[m.Ticket],
    limit_ticket: bool,
    sorting_type: str,
) -> list[m.Ticket]:
    is_reversed = True if sorting_type == m.TicketsSortingType.most_expensive.value else False
    tickets = sorted(tickets, key=lambda ticket: ticket.price_net if ticket.price_net else 0, reverse=is_reversed)

    if sorting_type == m.TicketsSortingType.category.value:
        tickets_sift = []
        categories_seen = set()
        for ticket in tickets:
            if ticket.event.category.name not in categories_seen:
                categories_seen.add(ticket.event.category.name)
                tickets_sift.append(ticket)
        tickets = tickets_sift

    if not limit_ticket:
        tickets = tickets[: app.config["TICKETS_PER_CHAT"]]

    return tickets


def book_ticket(
    ticket_unique_id: str,
    user: m.User,
    room: m.Room,
    limit_per_event: int,
) -> m.Ticket | s.BookTicketError:
    ticket_query = sa.select(m.Ticket).where(m.Ticket.unique_id == ticket_unique_id)
    ticket = db.session.scalar(ticket_query)

    tickets_per_event_query = sa.select(m.Ticket).where(
        sa.or_(m.Ticket.seller_id == user.id, m.Ticket.buyer_id == user.id),
        m.Ticket.event_id == ticket.event_id,
        m.Ticket.is_sold.is_(True),
    )
    tickets_per_event = db.session.scalars(tickets_per_event_query).all()
    if len(tickets_per_event) > limit_per_event:
        log(log.INFO, "Transactions per event limit reached: [%s]", ticket.event.name)
        return s.BookTicketError(
            limit_reached=True,
            error_message="You have reached the limit of tickets for this event",
        )

    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", ticket_unique_id)
        return s.BookTicketError(
            not_found=True,
            error_message="Something went wrong, please choose event again",
        )

    previous_tickets_query = sa.select(m.Ticket).where(
        m.Ticket.buyer_id == user.id,
        m.Ticket.is_reserved.is_(True),
        m.Ticket.is_sold.is_(False),
    )
    previous_tickets = db.session.scalars(previous_tickets_query).all()

    for previous_ticket in previous_tickets:
        previous_ticket.is_reserved = False
        previous_ticket.buyer_id = None
        previous_ticket.save(False)

    ticket.is_reserved = True
    ticket.last_reservation_time = datetime.now(UTC)
    ticket.buyer_id = user.id
    ticket.save(False)

    if ticket.is_paired and ticket.pair_unique_id:
        paired_ticket_query = sa.select(m.Ticket).where(m.Ticket.pair_unique_id == ticket.unique_id)
        paired_ticket = db.session.scalar(paired_ticket_query)
        paired_ticket.is_reserved = True
        paired_ticket.last_reservation_time = datetime.now(UTC)
        paired_ticket.buyer_id = user.id
        paired_ticket.save(False)

    room.ticket = ticket

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="We have found tickets. What ticket do you want?",
    ).save(False)
    m.Message(
        room_id=room.id,
        text="Ticket details:",
        details=True,
    ).save()

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

    global_fee_settings = db.session.scalar(sa.select(m.GlobalFeeSettings))
    service_fee = user.service_fee if user.service_fee is not None else global_fee_settings.service_fee
    bank_fee = user.bank_fee if user.bank_fee is not None else global_fee_settings.bank_fee
    total_commission = 1 + (service_fee + bank_fee) / 100

    price_total = 0
    price_service = 0
    price_net = 0
    unique_ids = ""
    for ticket in tickets:
        ticket_price_gross = ticket.price_net * total_commission
        ticket.price_gross = ticket_price_gross

        price_total += ticket_price_gross
        price_service += ticket_price_gross - ticket.price_net
        price_net += ticket.price_net
        unique_ids += f"{ticket.unique_id}, "
    return s.ChatBuyTicketTotalPrice(
        service=int(round(price_service)),
        total=int(round(price_total)),
        net=int(round(price_net)),
        unique_ids=unique_ids,
    )


def get_locations_by_events(events: list[m.Event], room: m.Room) -> list[m.Location] | None:
    events_names = [event.name for event in events]
    locations_query = sa.select(m.Location).filter(m.Location.events.any(m.Event.name.in_(events_names)))
    locations = db.session.scalars(locations_query).all()

    if not locations:
        log(log.INFO, "Locations not found: [%s]", events)

    return locations


def subscribe_event(event_unique_id: str, user: m.User) -> m.Event:
    event_query = sa.select(m.Event).where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", event_unique_id)
        return event

    if user not in event.subscribers:
        event.subscribers.append(user)
        event.save(False)
    if event not in user.subscribed_events:
        user.subscribed_events.append(event)
        user.save()

    return event


def create_user(email: str) -> m.User:
    user = m.User(
        email=email,
    )
    return user
