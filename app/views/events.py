from datetime import datetime

from flask import current_app as app
from flask import request, Blueprint, render_template

from app import schema as s
from app import models as m, db
from app.logger import log


events_blueprint = Blueprint("events", __name__, url_prefix="/events")


def get_filter_events():
    EVENTS_PER_PAGE: int = app.config["EVENTS_PER_PAGE"]
    events_on_page = EVENTS_PER_PAGE
    event_filter = s.EventFilter.model_validate(dict(request.args))
    categories = request.args.getlist("categories")
    date_format = "%m/%d/%Y"

    events_query = m.Event.select().limit(events_on_page)

    if event_filter.location:
        events_query = events_query.where(
            m.Event.location.has(name=event_filter.location)
        )

        log(log.INFO, "Applied location filter: [%s]", event_filter.location)
    if categories:
        events_query = events_query.filter(
            m.Event.category.has(m.Category.name.in_(categories))
        )

        log(log.INFO, "Applied categories filter: [%s]", categories)
    if event_filter.event_per_page:
        limit_events = event_filter.event_per_page
        limit_events += events_on_page
        events_query = events_query.limit(limit_events)

        log(
            log.INFO, "Applied event_per_page filter: [%s]", event_filter.event_per_page
        )
    if event_filter.date_from:
        date_from = datetime.strptime(event_filter.date_from, date_format)
        events_query = events_query.where(m.Event.date_time >= date_from)

        log(log.INFO, "Applied date_from filter: [%s]", event_filter.date_from)
    if event_filter.date_to:
        date_to = datetime.strptime(event_filter.date_to, date_format)
        events_query = events_query.where(m.Event.date_time <= date_to)

        log(log.INFO, "Applied date_to filter: [%s]", event_filter.date_to)

    events = db.session.scalars(events_query).all()

    log(log.INFO, "Return events from function: [%s]", events)
    return events


@events_blueprint.route("/", methods=["GET", "POST"])
def get_events():
    events = get_filter_events()
    categories = db.session.scalars(m.Category.select())
    locations = db.session.scalars(m.Location.select())

    log(log.INFO, "Render template events/events.html with events: [%s]", events)
    return render_template(
        "events/events.html", events=events, categories=categories, locations=locations
    )


@events_blueprint.route("/search")
def search_events():
    events = get_filter_events()

    log(log.INFO, "Render template events/events_list.html with events: [%s]", events)
    return render_template("events/events_list.html", events=events)
