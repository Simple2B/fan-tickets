from flask import render_template, Blueprint
from flask_login import login_required
from app import models as m


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
