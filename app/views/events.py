from flask import request, Blueprint, render_template
from app import models as m, db


events_blueprint = Blueprint("events", __name__, url_prefix="/events")


@events_blueprint.route("/", methods=["GET", "POST"])
def get_events():
    location_name = request.args.get("location")
    category_name = request.args.get("category")

    events_query = m.Event.select()

    if location_name:
        events_query = events_query.where(m.Event.location.has(name=location_name))
    if category_name:
        events_query = events_query.where(m.Event.category.has(name=category_name))

    events = db.session.scalars(events_query).all()
    return render_template("events/events.html", events=events)
