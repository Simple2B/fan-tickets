from datetime import datetime

import filetype
import sqlalchemy as sa

from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
)
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

    form = f.EventUpdateForm(category=event.category, location=event.location)
    form.category.choices = [(category.id, category.name) for category in db.session.scalars(m.Category.select())]
    form.location.choices = [(location.id, location.name) for location in db.session.scalars(m.Location.select())]

    if request.method == "GET":
        form.name.data = event.name
        form.url.data = event.url
        form.observations.data = event.observations
        form.date_time.data = event.date_time.date()
        form.warning.data = event.warning
        form.category.data = str(event.category_id)
        form.location.data = str(event.location_id)
        form.approved.data = event.approved

        log(log.INFO, "request.method = GET. Event form populated: [%s]", event)
        return render_template("admin/event.html", event=event, form=form)

    elif form.validate_on_submit():
        if db.session.scalar(sa.select(m.Event).where(m.Event.name == form.name.data)):
            log(log.WARNING, "Event already exists: [%s]", form.name.data)
            flash(f"Event already exists: {form.name.data}", "danger")
            render_template("admin/event.html", event=event, form=form)

        log(log.INFO, "Event form validated: [%s]", event)
        event.name = form.name.data
        event.url = form.url.data
        event.observations = form.observations.data
        event.warning = form.warning.data

        event.date_time = form.date_time.data
        event.category_id = int(form.category.data)
        event.location_id = int(form.location.data)
        event.approved = form.approved.data

        if form.picture.data:
            image_type = filetype.guess(form.picture.data.stream)
            if not image_type.mime.startswith("image"):
                log(log.WARNING, "File is not an image: [%s]", form.picture.data.filename)
                flash(f"Wrong image format: {image_type.mime}", "danger")
                return render_template("admin/event.html", event=event, form=form)

            picture = m.Picture(
                filename=form.picture.data.filename, mimetype=image_type.mime, file=form.picture.data.read()
            )

            if event.picture:
                db.session.delete(event.picture)

            event.picture = picture

        db.session.commit()
        log(log.INFO, "Event saved: [%s]", event)
        return redirect(url_for("admin.event.get_event", event_unique_id=event_unique_id))

    else:
        log(log.INFO, "Event form not validated: [%s]", form.errors)
        return render_template("admin/event.html", event=event, form=form)


@event_blueprint.route("/add_event", methods=["GET", "POST"])
@login_required
def add_event():
    form = f.EventForm()

    form.category.choices = [(category.id, category.name) for category in db.session.scalars(m.Category.select())]
    form.location.choices = [(location.id, location.name) for location in db.session.scalars(m.Location.select())]

    if request.method == "GET":
        form.date_time.data = datetime.now().date()
        return render_template("admin/event_add.html", form=form)

    if form.validate_on_submit():
        log(log.INFO, "Event form validated: [%s]", form)

        if db.session.scalar(sa.select(m.Event).where(m.Event.name == form.name.data)):
            log(log.WARNING, "Event already exists: [%s]", form.name.data)
            flash(f"Event already exists: {form.name.data}", "danger")
            return render_template("admin/event_add.html", form=form)

        event = m.Event(
            name=form.name.data,
            url=form.url.data,
            observations=form.observations.data,
            warning=form.warning.data,
            date_time=form.date_time.data,
            category_id=form.category.data,
            location_id=form.location.data,
            creator_id=current_user.id,
            approved=form.approved.data,
        ).save()
        log(log.INFO, "Event saved: [%s]", event)
        return redirect(url_for("admin.event.get_event", event_unique_id=event.unique_id))

    else:
        form.date_time.data = datetime.now().date()
        log(log.INFO, "Event form not validated: [%s]", form.errors)
        flash(form.errors, "danger")
        return render_template("admin/event_add.html", form=form)


@event_blueprint.route("/delete_event/<event_id>", methods=["GET"])
def delete_event(event_id: int):
    event = db.session.get(m.Event, event_id)
    if not event:
        log(log.INFO, "Event not found: [%s]", event_id)
        flash("Event not found", "danger")
        return redirect(url_for("admin.event.get_events"))

    if event.picture:
        db.session.delete(event.picture)

    db.session.delete(event)
    db.session.commit()

    return redirect(url_for("admin.event.get_events"))