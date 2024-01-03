from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from app import models as m, db
from app.controllers.image_upload import image_upload, ImageType
from app.logger import log


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprint.route("/")
@login_required
def admin():
    log(log.INFO, "Admin page requested by [%s]", current_user.id)
    return redirect(url_for("user.get_all"))


@admin_blueprint.route("/locations")
def get_locations():
    locations = m.Location.all()
    log(log.INFO, "Locations: [%s]", locations)
    return render_template("admin/locations.html", locations=locations)


@admin_blueprint.route("/categories")
def get_categories():
    categories = m.Category.all()
    log(log.INFO, "Categories: [%s]", categories)
    return render_template("admin/categories.html", categories=categories)


@admin_blueprint.route("/picture-upload", methods=["GET", "POST"])
@login_required
def picture_upload():
    user: m.User = current_user
    image_upload(user, ImageType.LOGO)
    return {}, 200


@admin_blueprint.route("/events")
def get_events():
    events = m.Event.all()
    return render_template("admin/events.html", events=events)


@admin_blueprint.route("/tickets")
def get_tickets():
    tickets = m.Ticket.all()
    return render_template("admin/tickets.html", tickets=tickets)


@admin_blueprint.route("/disputes")
def get_disputes():
    ticket_unique_id = request.args.get("ticket_unique_id")
    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    disputes_query = m.Room.select().where(m.Room.type_of == m.RoomType.DISPUTE.value)
    if ticket:
        disputes_query = disputes_query.where(m.Room.ticket_id == ticket.id)
    disputes = db.session.scalars(disputes_query).all()
    return render_template("admin/disputes.html", disputes=disputes)


@admin_blueprint.route("/notifications")
def get_notifications():
    notifications = m.Notification.all()
    return render_template("admin/notifications.html", notifications=notifications)
