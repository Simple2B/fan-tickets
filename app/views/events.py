from datetime import datetime
from typing import Any

from flask import request, Blueprint, render_template
import sqlalchemy as sa
from app import schema as s
from app import models as m, db
from app.logger import log

from config import config

CFG = config()


events_blueprint = Blueprint("events", __name__, url_prefix="/events")


def get_events_by_name(event_name: str) -> list[m.Event]:
    event_query = sa.select(m.Event).where(m.Event.name.ilike(f"%{event_name}%"))
    events = db.session.scalars(event_query).all()
    if events:
        return events

    search_key_words = event_name.split(" ") if event_name else []
    events = []
    for word in search_key_words:
        event_query = sa.select(m.Event).where(m.Event.name.ilike(f"%{word}%"))
        events_search = db.session.scalars(event_query).all()
        events.extend(events_search)

    return events


def get_filter_events():
    data: dict[str, Any] = dict(request.args)
    data["categories"] = request.args.getlist("categories")
    event_filter = s.EventFilter.model_validate(data)

    events_query = m.Event.select().where(m.Event.approved.is_(True), m.Event.date_time >= datetime.now())

    if event_filter.event_name:
        return get_events_by_name(event_filter.event_name)

    if event_filter.location:
        events_query = events_query.where(m.Event.location.has(name=event_filter.location))

        log(log.INFO, "Applied location filter: [%s]", event_filter.location)
    if event_filter.categories:
        events_query = events_query.filter(m.Event.category.has(m.Category.name.in_(event_filter.categories)))

        log(log.INFO, "Applied categories filter: [%s]", event_filter.categories)

    if event_filter.date_from:
        date_from = datetime.strptime(event_filter.date_from, CFG.DATE_PICKER_FORMAT)
        events_query = events_query.where(m.Event.date_time >= date_from)

        log(log.INFO, "Applied date_from filter: [%s]", event_filter.date_from)
    if event_filter.date_to:
        date_to = datetime.strptime(event_filter.date_to, CFG.DATE_PICKER_FORMAT)
        events_query = events_query.where(m.Event.date_time <= date_to)

        log(log.INFO, "Applied date_to filter: [%s]", event_filter.date_to)

    events: list[m.Event] = db.session.scalars(
        events_query.limit(event_filter.event_per_page + CFG.EVENTS_PER_PAGE)
    ).all()

    return events


@events_blueprint.route("/", methods=["GET", "POST"])
def get_events():
    events = get_filter_events()
    categories = db.session.scalars(m.Category.select())
    locations = db.session.scalars(m.Location.select()).all()

    log(log.INFO, "Render template events/events.html with events: [%s]", events)
    return render_template("events/events.html", events=events, categories=categories, locations=locations)


@events_blueprint.route("/search")
def search_events():
    events = get_filter_events()

    log(log.INFO, "Render template events/events_list.html with events: [%s]", events)
    return render_template("events/events_list.html", events=events)
