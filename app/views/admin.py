from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import models as m, db, forms as f
from app.controllers import create_pagination
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


@admin_blueprint.route("/add_location", methods=["GET", "POST"])
@login_required
def add_location():
    form = f.LocationForm()
    if request.method == "GET":
        return render_template("admin/location_add.html", form=form)

    if form.validate_on_submit():
        log(log.INFO, "Location form validated: [%s]", form)
        location = m.Location(
            name=form.name.data,
        ).save()
        log(log.INFO, "Location saved: [%s]", location)
        return redirect(url_for("admin.get_locations"))

    else:
        log(log.INFO, "Location form not validated: [%s]", form.errors)
        return render_template("admin/location_add.html", form=form)


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
        events_query = events_query.where(m.Event.creator.has(m.User.role == m.UserRole.client))
        count_query = count_query.where(m.Event.creator.has(m.User.role == m.UserRole.client))
    elif status == "admins":
        events_query = events_query.where(m.Event.creator.has(m.User.role == m.UserRole.admin))
        count_query = count_query.where(m.Event.creator.has(m.User.role == m.UserRole.admin))

    locations = db.session.scalars(locations_query).all()
    categories = db.session.scalars(categories_query).all()

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
            approved=True,
        ).save()
        log(log.INFO, "Event saved: [%s]", event)
        return redirect(url_for("admin.get_event", event_unique_id=event.unique_id))

    else:
        log(log.INFO, "Event form not validated: [%s]", form.errors)
        return render_template("admin/event_add.html", form=form)


@admin_blueprint.route("/tickets")
@login_required
def get_tickets():
    buyer_unique_id = request.args.get("buyer_unique_id")
    location_id = request.args.get("location_id")
    location_id = None if location_id == "all" else location_id
    date_from_str = request.args.get("date_from")
    date_to_str = request.args.get("date_to")
    ticket_type = request.args.get("ticket_type")
    ticket_type = None if ticket_type == "all" else ticket_type
    ticket_category = request.args.get("ticket_category")
    ticket_category = None if ticket_category == "all" else ticket_category

    tickets_query = m.Ticket.select().order_by(m.Ticket.created_at.desc())
    count_query = sa.select(sa.func.count()).select_from(m.Ticket)

    if buyer_unique_id:
        tickets_query = tickets_query.where(m.Ticket.buyer.has(m.User.unique_id == buyer_unique_id))
        count_query = count_query.where(m.Ticket.buyer.has(m.User.unique_id == buyer_unique_id))

    location_unique_id = None
    if location_id:
        tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.location_id == int(location_id)))
        location_unique_id = db.session.scalar(sa.select(m.Location.unique_id).where(m.Location.id == int(location_id)))
        count_query = count_query.where(m.Ticket.event.has(m.Event.location_id == int(location_id)))

    if date_from_str:
        date_from = datetime.strptime(date_from_str, "%m/%d/%Y")
        tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.date_time >= date_from))
        count_query = count_query.where(m.Ticket.event.has(m.Event.date_time >= date_from))

    if date_to_str:
        date_to = datetime.strptime(date_to_str, "%m/%d/%Y")
        tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.date_time <= date_to))
        count_query = count_query.where(m.Ticket.event.has(m.Event.date_time <= date_to))

    if ticket_type:
        tickets_query = tickets_query.where(m.Ticket.ticket_type == ticket_type)
        count_query = count_query.where(m.Ticket.ticket_type == ticket_type)

    if ticket_category:
        tickets_query = tickets_query.where(m.Ticket.ticket_category == ticket_category)
        count_query = count_query.where(m.Ticket.ticket_category == ticket_category)

    # tickets = db.session.scalars(tickets_query).all()
    ticket_types = [x.value for x in m.TicketType]
    ticket_categories = [x.value for x in m.TicketCategory]
    locations = m.Location.all()

    pagination = create_pagination(total=db.session.scalar(count_query))

    tickets_query = tickets_query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
    tickets = db.session.execute(
        tickets_query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
    ).scalars()

    return render_template(
        "admin/tickets.html",
        tickets=tickets,
        ticket_types=ticket_types,
        ticket_categories=ticket_categories,
        locations=locations,
        location_unique_id=location_unique_id,
        ticket_type_selected=ticket_type,
        ticket_category_selected=ticket_category,
        user_unique_id=buyer_unique_id,
        page=pagination,
    )


@admin_blueprint.route("/ticket/<ticket_unique_id>", methods=["GET", "POST"])
@login_required
def get_ticket(ticket_unique_id):
    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", ticket_unique_id)
        return redirect(url_for("admin.get_tickets"))

    form = f.TicketForm(ticket_type=ticket.ticket_type, ticket_category=ticket.ticket_category)
    if request.method == "GET":
        form.description.data = ticket.description
        form.warning.data = ticket.warning
        form.ticket_type.data = ticket.ticket_type
        form.ticket_category.data = ticket.ticket_category
        form.section.data = ticket.section
        form.queue.data = ticket.queue
        form.seat.data = ticket.seat
        form.price_net.data = ticket.price_net
        form.price_gross.data = ticket.price_gross

        log(log.INFO, "request.method = GET. Ticket form populated: [%s]", ticket)
        return render_template("admin/ticket.html", ticket=ticket, form=form)

    if form.validate_on_submit():
        log(log.INFO, "Ticket form validated: [%s]", ticket)
        ticket.description = form.description.data
        ticket.warning = form.warning.data
        ticket.ticket_type = form.ticket_type.data
        ticket.ticket_category = form.ticket_category.data
        ticket.section = form.section.data
        ticket.queue = form.queue.data
        ticket.seat = form.seat.data
        ticket.price_net = form.price_net.data
        ticket.save()
        log(log.INFO, "Ticket saved: [%s]", ticket)
        return redirect(url_for("admin.get_ticket", ticket_unique_id=ticket_unique_id))

    else:
        log(log.INFO, "Ticket form not validated: [%s]", form.errors)
        return render_template("admin/ticket.html", ticket=ticket, form=form)


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
