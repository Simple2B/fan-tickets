from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from app import models as m, db, forms as f
from app.controllers.image_upload import image_upload, ImageType
from app.logger import log


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprint.route("/")
@login_required
def admin():
    log(log.INFO, "Admin page requested by [%s]", current_user.id)
    return redirect(url_for("user.get_all"))


@admin_blueprint.route("/locations")
@login_required
def get_locations():
    locations = m.Location.all()
    log(log.INFO, "Locations: [%s]", locations)
    return render_template("admin/locations.html", locations=locations)


@admin_blueprint.route("/categories")
@login_required
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
@login_required
def get_events():
    # TODO pending events, added by users, added by admin
    events_query = m.Event.select().order_by(m.Event.date_time.desc())
    events = db.session.scalars(events_query).all()
    locations = m.Location.all()
    categories = m.Category.all()
    return render_template(
        "admin/events.html",
        events=events,
        locations=locations,
        categories=categories,
    )


@admin_blueprint.route("/event/<event_unique_id>", methods=["GET", "POST"])
@login_required
def get_event(event_unique_id):
    event_query = m.Event.select().where(m.Event.unique_id == event_unique_id)
    event: m.Event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", event_unique_id)
        return redirect(url_for("admin.get_events"))

    form = f.EventForm(category=event.category, location=event.location)
    if request.method == "GET":
        form.name.data = event.name
        form.url.data = event.url
        form.observations.data = event.observations
        form.warning.data = event.warning

        date_time_str = event.date_time.strftime("%m/%d/%Y")
        form.date_time.data = date_time_str
        # form.category.data = event.category_id
        # form.location.data = event.location_id

        log(log.INFO, "request.method = GET. Event form populated: [%s]", event)
        return render_template("admin/event.html", event=event, form=form)

    if form.validate_on_submit():
        log(log.INFO, "Event form validated: [%s]", event)
        event.name = form.name.data
        event.url = form.url.data
        event.observations = form.observations.data
        event.warning = form.warning.data

        date_time_data = datetime.strptime(form.date_time.data, "%m/%d/%Y")
        event.date_time = date_time_data
        event.category_id = form.category.data
        event.location_id = form.location.data
        event.save()
        log(log.INFO, "Event saved: [%s]", event)
        return redirect(url_for("admin.get_event", event_unique_id=event_unique_id))

    else:
        log(log.INFO, "Event form not validated: [%s]", form.errors)
        return render_template("admin/event.html", event=event, form=form)


@admin_blueprint.route("/add_event", methods=["GET", "POST"])
@login_required
def add_event():
    form = f.EventForm()
    if request.method == "GET":
        return render_template("admin/event_add.html", form=form)

    if form.validate_on_submit():
        log(log.INFO, "Event form validated: [%s]", form)
        event = m.Event(
            name=form.name.data,
            url=form.url.data,
            observations=form.observations.data,
            warning=form.warning.data,
            date_time=form.date_time.data,
            category_id=form.category.data,
            location_id=form.location.data,
            creator_id=current_user.id,
        ).save()
        log(log.INFO, "Event saved: [%s]", event)
        return redirect(url_for("admin.get_event", event_unique_id=event.unique_id))

    else:
        log(log.INFO, "Event form not validated: [%s]", form.errors)
        return render_template("admin/event_add.html", form=form)


@admin_blueprint.route("/tickets")
@login_required
def get_tickets():
    tickets = m.Ticket.all()
    return render_template("admin/tickets.html", tickets=tickets)


@admin_blueprint.route("/disputes")
@login_required
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
@login_required
def get_notifications():
    notifications = m.Notification.all()
    return render_template("admin/notifications.html", notifications=notifications)
