import os
from bardapi import Bard
import sqlalchemy as sa
from flask import request, render_template, Blueprint
from flask_login import login_required
from app import schemas as s
from app import models as m, db


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    users_number = m.User.count()
    locations_number = m.Location.count()
    categories_number = m.Category.count()
    events_number = m.Event.count()
    tickets_number = m.Ticket.count()
    reviews_number = m.Review.count()
    disputes_number = m.Dispute.count()
    notifications_number = m.Notification.count()
    rooms_number = m.Room.count()
    messages_number = m.Message.count()
    return render_template(
        "index.html",
        users_number=users_number,
        locations_number=locations_number,
        categories_number=categories_number,
        events_number=events_number,
        tickets_number=tickets_number,
        reviews_number=reviews_number,
        disputes_number=disputes_number,
        notifications_number=notifications_number,
        rooms_number=rooms_number,
        messages_number=messages_number,
    )


@main_blueprint.route("/locations")
def get_locations():
    locations = m.Location.all()
    return render_template("demo/locations.html", locations=locations)


@main_blueprint.route("/categories")
def get_categories():
    categories = m.Category.all()
    return render_template("demo/categories.html", categories=categories)


@main_blueprint.route("/events")
def get_events():
    events = m.Event.all()
    return render_template("demo/events.html", events=events)


@main_blueprint.route("/tickets")
def get_tickets():
    tickets = m.Ticket.all()
    return render_template("demo/tickets.html", tickets=tickets)


@main_blueprint.route("/reviews")
def get_reviews():
    reviews = m.Review.all()
    return render_template("demo/reviews.html", reviews=reviews)


@main_blueprint.route("/disputes")
def get_disputes():
    disputes = m.Dispute.all()
    return render_template("demo/disputes.html", disputes=disputes)


@main_blueprint.route("/notifications")
def get_notifications():
    notifications = m.Notification.all()
    return render_template("demo/notifications.html", notifications=notifications)


@main_blueprint.route("/room/<room_unique_id>")
def get_room(room_unique_id: str):
    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    return render_template("demo/room.html", room=room)


@main_blueprint.route("/whatsapp", methods=["GET", "POST"])
def get_events_json():
    user_id = request.json.get("user_id")
    token = request.json.get("token")
    location = request.json.get("location")
    date_from = request.json.get("date_from")
    date_to = request.json.get("date_to")

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
    events_list = s.Events(events=events, user_id=user_id).json()

    os.environ[
        "_BARD_API_KEY"
    ] = "cQjl3nIkpG3rTz3hEgPC4EB1pcyHBGcFbAU0_8ah4S7-8_ZXTk6QPdaPJzbJIeJXIFADfg."

    events_list = {"some_data": "some_data"}

    message = f"Could you please make a human readable answer of the following JSON? {events_list}"

    bard = Bard()

    answer = bard.get_answer(message).get("content")

    return {"answer": answer}
