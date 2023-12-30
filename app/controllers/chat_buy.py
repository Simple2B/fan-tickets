from datetime import datetime
from random import randint
import re

import sqlalchemy as sa

from flask import current_app as app


from werkzeug.security import check_password_hash

from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db

from app.logger import log


def get_event_by_name(event_name: str, room: m.Room) -> m.Event | None:
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


def get_tickets_by_event(event: m.Event, room: m.Room) -> list[m.Ticket] | None:
    tickets_query = sa.select(m.Ticket).where(m.Ticket.event_id == event.id)
    tickets = db.session.scalars(tickets_query).all()

    if not tickets:
        log(log.INFO, "Tickets not found: [%s]", event.name)
        c.save_message(
            "Great! To get started, could you please write below name of the event you're looking for?",
            f"{event.name}",
            room,
        )
    return tickets


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
