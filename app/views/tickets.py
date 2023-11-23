from flask import request, Blueprint, render_template
from app import models as m, db


tickets_blueprint = Blueprint("tickets", __name__, url_prefix="/tickets")


@tickets_blueprint.route("/", methods=["GET", "POST"])
def get_all():
    tickets_limit = 10
    if request.args.get("tickets_per_page"):
        tickets_limit += int(request.args.get("tickets_per_page"))
    location_name = request.args.get("location")
    category_name = request.args.get("categories")
    tickets_query = m.Ticket.select().limit(tickets_limit)

    if location_name:
        location_query = m.Location.select().where(m.Location.name == location_name)
        location = db.session.scalar(location_query)
        tickets_query = tickets_query.where(m.Ticket.event.has(location_id=location.id))

    if category_name:
        category_query = m.Category.select().where(m.Category.name == category_name)
        category = db.session.scalar(category_query)
        tickets_query = tickets_query.where(m.Ticket.event.has(category_id=category.id))

    if request.args.get("date_from"):
        tickets_query = tickets_query.where(
            m.Ticket.event.date_time >= request.args.get("date_from")
        )
    if request.args.get("date_to"):
        tickets_query = tickets_query.where(
            m.Ticket.event.date_time <= request.args.get("date_to")
        )
    categories = db.session.scalars(m.Category.select())
    locations = db.session.scalars(m.Location.select())
    tickets = db.session.scalars(tickets_query).all()

    if (
        request.args.get("categories")
        or request.args.get("location")
        or request.args.get("date_from")
        or request.args.get("date_to")
        or request.args.get("tickets_per_page")
    ):
        template = "tickets/tickets_list.html"
    else:
        template = "tickets/tickets.html"

    return render_template(
        template,
        tickets=tickets,
        categories=categories,
        locations=locations,
    )
