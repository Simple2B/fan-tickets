from typing import Any
from datetime import datetime
from flask import request, Blueprint, render_template
from app import models as m, db
from app import schema as s

from config import config

CFG = config()


tickets_blueprint = Blueprint("tickets", __name__, url_prefix="/tickets")


def get_all_tickets(filter: s.TicketFilter) -> list[m.Ticket]:
    tickets_query = m.Ticket.select()

    if filter.event_id:
        tickets_query = tickets_query.where(m.Ticket.event_id == filter.event_id)
    else:
        if filter.q:
            tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.name.ilike(f"%{filter.q}%")))

        if filter.location:
            location_query = m.Location.select().where(m.Location.name == filter.location)
            location = db.session.scalar(location_query)
            tickets_query = tickets_query.where(m.Ticket.event.has(location_id=location.id))

        if filter.categories:
            tickets_query = tickets_query.filter(
                m.Ticket.event.has(m.Event.category.has(m.Category.name.in_(filter.categories)))
            )

        if filter.date_from:
            date_from = datetime.strptime(filter.date_from, CFG.DATE_PICKER_FORMAT)
            tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.date_time >= date_from))
        if filter.date_to:
            date_to = datetime.strptime(filter.date_to, CFG.DATE_PICKER_FORMAT)
            tickets_query = tickets_query.where(m.Ticket.event.has(m.Event.date_time <= date_to))

    limit = filter.tickets_per_page + CFG.TICKETS_PER_PAGE
    if filter.tickets_number:
        limit = filter.tickets_number + CFG.TICKETS_PER_PAGE

    return db.session.scalars(tickets_query.limit(limit)).all()


@tickets_blueprint.route("/", methods=["GET", "POST"])
def get_all():
    data: dict[str, Any] = dict(request.args)
    data["categories"] = request.args.getlist("categories")
    filter = s.TicketFilter.model_validate(data)

    tickets = get_all_tickets(filter)

    if (
        filter.q
        or filter.location
        or filter.date_from
        or filter.date_to
        or filter.categories
        or filter.tickets_per_page
        or filter.tickets_number
    ):
        template = "tickets/tickets_list.html"
    else:
        template = "tickets/tickets.html"

    return render_template(
        template,
        tickets=tickets,
        tickets_number=len(tickets),
        categories=m.Category.all(),
        locations=m.Location.all(),
    )


@tickets_blueprint.route("/<int:ticket_unique_id>")
def get_ticket(ticket_unique_id: str):
    ticket_query = m.Ticket.select().where(m.Ticket.id == 1)
    ticket = db.session.scalar(ticket_query)

    return render_template("tickets/ticket.html", ticket=ticket)
