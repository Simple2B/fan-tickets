import io
from datetime import datetime, time, UTC
import csv
import filetype
import sqlalchemy as sa

from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    send_file,
)
from flask_login import current_user
from app.controllers import create_pagination

from app import models as m
from app import forms as f
from app.database import db
from app.logger import log

event_blueprint = Blueprint("event", __name__, url_prefix="/event")


@event_blueprint.route("/events")
def get_events():
    # Filters
    q = request.args.get("q")
    search = request.args.get("search")
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
    count_query = sa.select(sa.func.count()).select_from(m.Event)
    locations_query = m.Location.select()
    categories_query = m.Category.select()

    template = "admin/events.html"
    if q or search:
        events_query = events_query.where(m.Event.name.ilike(f"%{q}%"))
        count_query = count_query.where(m.Event.name.ilike(f"%{q}%"))
        template = "admin/events_list.html"

    location_unique_id = None
    if location_id:
        events_query = events_query.where(m.Event.location_id == int(location_id))
        count_query = count_query.where(m.Event.location_id == int(location_id))
        location_unique_id = db.session.scalar(sa.select(m.Location.unique_id).where(m.Location.id == int(location_id)))

    if date_from_str:
        date_from = datetime.strptime(date_from_str, "%m/%d/%Y")
        events_query = events_query.where(m.Event.date_time >= date_from)
        count_query = count_query.where(m.Event.date_time >= date_from)

    if date_to_str:
        date_to = datetime.strptime(date_to_str, "%m/%d/%Y")
        events_query = events_query.where(m.Event.date_time <= date_to)
        count_query = count_query.where(m.Event.date_time <= date_to)

    category_selected = None
    if category_id:
        events_query = events_query.where(m.Event.category_id == int(category_id))
        count_query = count_query.where(m.Event.category_id == int(category_id))
        category_selected = db.session.scalar(sa.select(m.Category.name).where(m.Category.id == int(category_id)))

    if status == "pending":
        events_query = events_query.where(m.Event.approved.is_(False))
        count_query = count_query.where(m.Event.approved.is_(False))
    elif status == "users":
        events_query = events_query.where(m.Event.creator.has(m.User.role == m.UserRole.client.value))
        count_query = count_query.where(m.Event.creator.has(m.User.role == m.UserRole.client.value))
    elif status == "admins":
        events_query = events_query.where(m.Event.creator.has(m.User.role == m.UserRole.admin.value))
        count_query = count_query.where(m.Event.creator.has(m.User.role == m.UserRole.admin.value))

    locations = db.session.scalars(locations_query).all()
    categories = db.session.scalars(categories_query).all()

    # Download
    if request.args.get("download"):
        log(log.INFO, "Downloading events table")
        events = db.session.scalars(events_query).all()
        with io.StringIO() as proxy:
            writer = csv.writer(proxy)
            row = [
                "#",
                "name",
                "URL",
                "Date",
                "Time",
                "Days from now",
                "Created by",
                "Approved",
                "Observations",
                "Warning",
                "Category",
                "Location",
                "Venue",
                "Tickets",
            ]
            writer.writerow(row)
            for index, event in enumerate(events):
                event_date = event.date_time.strftime("%m/%d/%Y")
                event_time = event.date_time.strftime("%H:%M")
                row = [
                    str(index),
                    event.name,
                    event.url,
                    event_date,
                    event_time,
                    (event.date_time - datetime.now(UTC)).days,
                    event.creator.email,
                    event.approved,
                    event.observations,
                    event.warning,
                    event.category.name,
                    event.location.name,
                    event.venue,
                    str(len(event.tickets)),
                ]
                writer.writerow(row)

            mem = io.BytesIO()
            mem.write(proxy.getvalue().encode("utf-8"))
            mem.seek(0)

        now = datetime.now()
        return send_file(
            mem,
            as_attachment=True,
            download_name=f"fan_ticket_events_{now.strftime('%Y-%m-%d-%H-%M-%S')}.csv",
            mimetype="text/csv",
            max_age=0,
            last_modified=now,
        )

    pagination = create_pagination(total=db.session.scalar(count_query))

    events_query = events_query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
    events = db.session.execute(
        events_query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
    ).scalars()

    return render_template(
        template,
        events=events,
        locations=locations,
        categories=categories,
        location_unique_id=location_unique_id,
        category_selected=category_selected,
        status_selected=status,
        page=pagination,
        q=q,
        location_id=location_id,
        date_from=date_from_str,
        date_to=date_to_str,
        category_id=category_id,
    )


@event_blueprint.route("/event/<event_unique_id>", methods=["GET", "POST"])
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
        form.venue.data = event.venue
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

        event.date_time = datetime.combine(form.date_time.data, time(hour=form.hours.data, minute=form.minutes.data))
        event.category_id = int(form.category.data)
        event.location_id = int(form.location.data)
        event.venue = form.venue.data
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

        event_date_time = datetime.combine(form.date_time.data, time(hour=form.hours.data, minute=form.minutes.data))
        event = m.Event(
            name=form.name.data,
            url=form.url.data,
            observations=form.observations.data,
            warning=form.warning.data,
            date_time=event_date_time,
            category_id=form.category.data,
            location_id=form.location.data,
            venue=form.venue.data,
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
