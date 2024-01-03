from flask import render_template, Blueprint
from app import models as m, db


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    events = db.session.scalars(m.Event.select().limit(8)).all()
    locations = db.session.scalars(m.Location.select()).all()
    return render_template(
        "landing/home/index.html",
        events=events,
        locations=locations,
    )


@main_blueprint.route("/help")
def help():
    return render_template("help.html")


@main_blueprint.route("/locations")
def get_locations():
    locations = m.Location.all()
    return render_template("admin/locations.html", locations=locations)


@main_blueprint.route("/categories")
def get_categories():
    categories = m.Category.all()
    return render_template("admin/categories.html", categories=categories)


@main_blueprint.route("/events")
def get_events():
    events = m.Event.all()
    return render_template("events/events.html", events=events)


@main_blueprint.route("/tickets")
def get_tickets():
    tickets = m.Ticket.all()
    return render_template("admin/tickets.html", tickets=tickets)


@main_blueprint.route("/reviews")
def get_reviews():
    reviews = m.Review.all()
    return render_template("admin/reviews.html", reviews=reviews)


@main_blueprint.route("/disputes")
def get_disputes():
    disputes_query = m.Room.select().where(m.Room.type_of == m.RoomType.DISPUTE.value)
    disputes = db.session.scalars(disputes_query).all()
    return render_template("admin/disputes.html", disputes=disputes)


@main_blueprint.route("/notifications")
def get_notifications():
    notifications = m.Notification.all()
    return render_template("admin/notifications.html", notifications=notifications)
