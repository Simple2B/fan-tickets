from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user


from app import models as m
from app import forms as f
from app.database import db
from app.logger import log

event_blueprint = Blueprint("event", __name__, url_prefix="/event")


@event_blueprint.route("/events")
@login_required
def get_events():
    # Filters
    # TODO replace by pydantic args
    location_id = request.args.get("location_id")
    location_id = None if location_id == "all" else location_id
    date_from_str = request.args.get("date_from")
    date_to_str = request.args.get("date_to")
    category_id = request.args.get("category_id")
    category_id = None if category_id == "all" else category_id
    status = request.args.get("status")
    status = None if status == "all" else status

    # Query for all events
    events_query = m.Event.select().order_by(m.Event.date_time.desc())
    locations_query = m.Location.select()
    categories_query = m.Category.select()

    if location_id:
        events_query = events_query.where(m.Event.location_id == int(location_id))

    if date_from_str:
        date_from = datetime.strptime(date_from_str, "%m/%d/%Y")
        events_query = events_query.where(m.Event.date_time >= date_from)

    if date_to_str:
        date_to = datetime.strptime(date_to_str, "%m/%d/%Y")
        events_query = events_query.where(m.Event.date_time <= date_to)

    if category_id:
        events_query = events_query.where(m.Event.category_id == int(category_id))

    if status == "pending":
        events_query = events_query.where(m.Event.approved.is_(False))
    elif status == "users":
        events_query = events_query.where(m.Event.creator.has(m.User.role == m.UserRole.client))
    elif status == "admins":
        events_query = events_query.where(m.Event.creator.has(m.User.role == m.UserRole.admin))

    events = db.session.scalars(events_query).all()
    locations = db.session.scalars(locations_query).all()
    categories = db.session.scalars(categories_query).all()
    return render_template(
        "admin/events.html",
        events=events,
        locations=locations,
        categories=categories,
    )


@event_blueprint.route("/event/<event_unique_id>", methods=["GET", "POST"])
@login_required
def get_event(event_unique_id):
    event_query = m.Event.select().where(m.Event.unique_id == event_unique_id)
    event: m.Event = db.session.scalar(event_query)

    if not event:
        log(log.INFO, "Event not found: [%s]", event_unique_id)
        return redirect(url_for("admin.event.get_events"))

    form = f.EventForm(category=event.category, location=event.location)
    if request.method == "GET":
        form.name.data = event.name
        form.url.data = event.url
        form.observations.data = event.observations
        form.warning.data = event.warning

        date_time_str = event.date_time.strftime("%m/%d/%Y")
        form.date_time.data = date_time_str
        form.approved.data = event.approved

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
        event.approved = True if form.approved.data == "True" else False
        event.save()
        log(log.INFO, "Event saved: [%s]", event)
        return redirect(url_for("admin.event.get_event", event_unique_id=event_unique_id))

    else:
        log(log.INFO, "Event form not validated: [%s]", form.errors)
        return render_template("admin/event.html", event=event, form=form)


@event_blueprint.route("/add_event", methods=["GET", "POST"])
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
            approved=True,
        ).save()
        log(log.INFO, "Event saved: [%s]", event)
        return redirect(url_for("admin.event.get_event", event_unique_id=event.unique_id))

    else:
        log(log.INFO, "Event form not validated: [%s]", form.errors)
        return render_template("admin/event_add.html", form=form)
