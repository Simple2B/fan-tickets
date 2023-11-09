import sqlalchemy as sa
from flask import request, Blueprint
from app import schema as s
from app import models as m, db


events_blueprint = Blueprint("events", __name__, url_prefix="/events")


@events_blueprint.route("/", methods=["GET", "POST"])
def get_events():
    user_id = request.json.get("user_id")
    token = request.json.get("token")
    location = request.json.get("location")
    date_from = request.json.get("date_from")
    date_to = request.json.get("date_to")

    if not user_id:
        return (
            s.GenericError(error="BAD_REQUEST", details="Missing user_id").dict(),
            400,
        )
    if not token == "testing_whatsapp_token":
        return {"error": "Invalid token"}, 403
    if not location:
        return {"error": "Missing location"}, 400
    if not date_from:
        return {"error": "Missing date_from"}, 400
    if not date_to:
        return {"error": "Missing date_to"}, 400

    events_query_by_location = sa.select(m.Event).where(
        m.Event.location.has(m.Location.name == location)
    )
    events = db.session.scalars(events_query_by_location).all()
    return s.Events(events=events, user_id=user_id).dict()


@events_blueprint.route("/by_id")
def get_event_by_id():
    event_unique_id = request.args.get("event_unique_id")
    event_query = sa.select(m.Event).where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        return {"error": "Event not found"}, 404
    return s.Event.from_orm(event).dict()
