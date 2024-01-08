from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from app import models as m, db, forms as f
from app.controllers.image_upload import image_upload, ImageType
from app.logger import log


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprint.before_request
def check_if_user_is_admin():
    if current_user.role != m.UserRole.admin.value:
        return redirect(url_for("main.index"))


@admin_blueprint.route("/")
@login_required
def admin():
    log(log.INFO, "Admin page requested by [%s]", current_user.id)
    return redirect(url_for("user.get_all"))


@admin_blueprint.route("/picture-upload", methods=["GET", "POST"])
@login_required
def picture_upload():
    user: m.User = current_user
    image_upload(user, ImageType.LOGO)
    return {}, 200


@admin_blueprint.route("/tickets")
@login_required
def get_tickets():
    tickets = m.Ticket.all()
    ticket_types = [x.value for x in m.TicketType]
    ticket_categories = [x.value for x in m.TicketCategory]
    return render_template(
        "admin/tickets.html",
        tickets=tickets,
        ticket_types=ticket_types,
        ticket_categories=ticket_categories,
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
