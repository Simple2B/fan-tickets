from flask import request, Blueprint, render_template
from app import models as m, db


events_blueprint = Blueprint("events", __name__, url_prefix="/events")


@events_blueprint.route("/", methods=["GET", "POST"])
def get_events():
    category_name = request.args.get("category")

    events_query = m.Event.select()

    if category_name:
        events_query = events_query.where(m.Event.category.has(name=category_name))

    events = db.session.scalars(events_query).all()
    return render_template("events/events.html", events=events)
