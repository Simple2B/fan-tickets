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
    return render_template("demo/locations.html", locations=locations)


@main_blueprint.route("/categories")
def get_categories():
    categories = m.Category.all()
    return render_template("demo/categories.html", categories=categories)


@main_blueprint.route("/events")
def get_events():
    events = m.Event.all()
    return render_template("events/events.html", events=events)


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
