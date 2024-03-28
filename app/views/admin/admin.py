import io
import csv
from datetime import datetime, UTC
from flask import Blueprint, redirect, url_for, render_template, request, jsonify, send_file
from flask_login import current_user
import sqlalchemy as sa
from app import models as m, db, forms as f
from app.controllers import create_pagination
from app.controllers.image_upload import image_upload, ImageType
from app.logger import log


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprint.before_request
def check_if_user_is_admin():
    if current_user.is_anonymous or current_user.role != m.UserRole.admin.value:
        return redirect(url_for("main.index"))


@admin_blueprint.route("/")
def admin():
    log(log.INFO, "Admin page requested by [%s]", current_user.id)
    return redirect(url_for("admin.user.get_all"))


@admin_blueprint.route("/picture-upload", methods=["GET", "POST"])
def picture_upload():
    user: m.User = current_user
    image_upload(user, ImageType.LOGO)
    return jsonify({})


@admin_blueprint.route("/tickets")
def get_tickets():
    q = request.args.get("q", "")
    search = request.args.get("search")
    buyer_unique_id = request.args.get("buyer_unique_id")
    seller_unique_id = request.args.get("seller_unique_id")
    location_id = request.args.get("location_id")
    location_id = None if location_id == "all" or location_id == "None" else location_id
    date_from_str = request.args.get("date_from")
    date_from_str = None if date_from_str == "all" or date_from_str == "None" else date_from_str
    date_to_str = request.args.get("date_to")
    date_to_str = None if date_to_str == "all" or date_to_str == "None" else date_to_str
    ticket_type = request.args.get("ticket_type")
    ticket_type = None if ticket_type == "all" or ticket_type == "None" else ticket_type
    ticket_category = request.args.get("ticket_category")
    ticket_category = None if ticket_category == "all" or ticket_category == "None" else ticket_category

    tickets_query = m.Ticket.select().where(m.Ticket.is_deleted.is_(False)).order_by(m.Ticket.created_at.desc())
    count_query = sa.select(sa.func.count()).select_from(m.Ticket)

    if buyer_unique_id:
        tickets_query = tickets_query.where(m.Ticket.buyer.has(m.User.uuid == buyer_unique_id))
        count_query = count_query.where(m.Ticket.buyer.has(m.User.uuid == buyer_unique_id))

    if seller_unique_id:
        tickets_query = tickets_query.where(m.Ticket.seller.has(m.User.uuid == seller_unique_id))
        count_query = count_query.where(m.Ticket.seller.has(m.User.uuid == seller_unique_id))

    location_unique_id = None
    if location_id:
        tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.location_id == int(location_id)))
        location_unique_id = db.session.scalar(sa.select(m.Location.unique_id).where(m.Location.id == int(location_id)))
        count_query = count_query.where(m.Ticket.event.has(m.Event.location_id == int(location_id)))

    if date_from_str:
        date_from = datetime.strptime(date_from_str, "%d/%m/%Y")
        tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.date_time >= date_from))
        count_query = count_query.where(m.Ticket.event.has(m.Event.date_time >= date_from))

    if date_to_str:
        date_to = datetime.strptime(date_to_str, "%d/%m/%Y")
        tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.date_time <= date_to))
        count_query = count_query.where(m.Ticket.event.has(m.Event.date_time <= date_to))

    if ticket_type:
        tickets_query = tickets_query.where(m.Ticket.ticket_type == ticket_type)
        count_query = count_query.where(m.Ticket.ticket_type == ticket_type)

    if ticket_category:
        tickets_query = tickets_query.where(m.Ticket.ticket_category == ticket_category)
        count_query = count_query.where(m.Ticket.ticket_category == ticket_category)

    ticket_types = [x.value for x in m.TicketType]
    ticket_categories = [x.value for x in m.TicketCategory]
    locations = m.Location.all()

    if q or search:
        try:
            ticket_id = int(q)
            tickets_query = tickets_query.where(m.Ticket.id == ticket_id)
            count_query = count_query.where(m.Ticket.id == ticket_id)
        except Exception:
            log(log.INFO, "Invalid ticket id: [%s]", q)
        template = "admin/tickets_list.html"
    else:
        template = "admin/tickets.html"

    # Download
    if request.args.get("download"):
        log(log.INFO, "Downloading events table")
        tickets = db.session.scalars(tickets_query).all()
        with io.StringIO() as proxy:
            writer = csv.writer(proxy)
            row = [
                "#",
                "ID",
                "name",
                "URL",
                "Date",
                "Time",
                "Days from now",
                "Type",
                "Category",
                "Description",
                "Warning",
                "Location",
                "Venue",
                "Seller",
                "Section",
                "Queue",
                "Seat",
                "Price net",
                "Price gross",
                "Is sold",
                "Buyer",
            ]
            writer.writerow(row)
            for index, ticket in enumerate(tickets):
                ticket_date = ticket.event.date_time.strftime("%m/%d/%Y")
                ticket_time = ticket.event.date_time.strftime("%H:%M")
                row = [
                    str(index),
                    str(ticket.id).zfill(8),
                    ticket.event.name,
                    ticket.event.url,
                    ticket_date,
                    ticket_time,
                    (ticket.event.date_time - datetime.now(UTC)).days,
                    ticket.ticket_type,
                    ticket.ticket_category,
                    ticket.description,
                    ticket.warning,
                    ticket.event.location.name,
                    ticket.event.venue,
                    ticket.seller.email,
                    ticket.section,
                    ticket.queue,
                    ticket.seat,
                    ticket.price_net,
                    ticket.price_gross,
                    ticket.is_sold,
                    ticket.buyer.email,
                ]
                writer.writerow(row)

            mem = io.BytesIO()
            mem.write(proxy.getvalue().encode("utf-8"))
            mem.seek(0)

        now = datetime.now()
        return send_file(
            mem,
            as_attachment=True,
            download_name=f"fan_ticket_tickets_{now.strftime('%Y-%m-%d-%H-%M-%S')}.csv",
            mimetype="text/csv",
            max_age=0,
            last_modified=now,
        )

    pagination = create_pagination(total=db.session.scalar(count_query))

    tickets_query = tickets_query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
    tickets = db.session.execute(
        tickets_query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
    ).scalars()

    return render_template(
        template,
        tickets=tickets,
        ticket_types=ticket_types,
        ticket_categories=ticket_categories,
        locations=locations,
        location_unique_id=location_unique_id,
        ticket_type_selected=ticket_type,
        ticket_category_selected=ticket_category,
        user_unique_id=buyer_unique_id,
        page=pagination,
        buyer_unique_id=buyer_unique_id,
        seller_unique_id=seller_unique_id,
        date_from=date_from_str,
        date_to=date_to_str,
        location_id=location_id,
        q=q,
    )


@admin_blueprint.route("/ticket/<ticket_unique_id>", methods=["GET", "POST"])
def get_ticket(ticket_unique_id):
    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    if not ticket:
        log(log.INFO, "Ticket not found: [%s]", ticket_unique_id)
        return redirect(url_for("admin.get_tickets"))

    form = f.TicketForm(
        ticket_type=ticket.ticket_type,
        ticket_category=ticket.ticket_category,
        ticket_deleted=ticket.is_deleted,
    )
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
        form.deleted.data = ticket.is_deleted

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
    return "notification template"
