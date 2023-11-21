from flask import request, Blueprint, render_template
from app import models as m, db
from app import schema as s


events_blueprint = Blueprint("events", __name__, url_prefix="/events")


def get_filter_events():
    events_per_page = 3
    event_filter = s.EventFilter.model_validate(dict(request.args))
    categories = request.args.getlist("categories")

    events_query = m.Event.select().limit(events_per_page)

    if event_filter.location:
        events_query = events_query.where(
            m.Event.location.has(name=event_filter.location)
        )
    if len(categories) > 0:
        events_query = events_query.where(
            m.Event.category.has(m.Category.name in categories)
        )
    if event_filter.event_per_page:
        limit_events = event_filter.event_per_page
        limit_events += events_per_page
        events_query = events_query.limit(limit_events)

    if event_filter.date_from:
        events_query = events_query.where(m.Event.date_time >= event_filter.date_from)

    if event_filter.date_to:
        events_query = events_query.where(m.Event.date_time <= event_filter.date_to)

    events = db.session.scalars(events_query).all()

    return events


@events_blueprint.route("/", methods=["GET", "POST"])
def get_events():
    events = get_filter_events()
    categories = db.session.scalars(m.Category.select()).all()
    locations = db.session.scalars(m.Location.select()).all()

    return render_template(
        "events/events.html", events=events, categories=categories, locations=locations
    )


@events_blueprint.route("/search")
def search_events():
    events = get_filter_events()

    return render_template("events/events_list.html", events=events)
