from flask import request, Blueprint, render_template
from app import models as m, db


tickets_blueprint = Blueprint("tickets", __name__, url_prefix="/tickets")


@tickets_blueprint.route("/", methods=["GET", "POST"])
def get_all():
    search_query = request.args.get("q")
    tickets_limit = 10
    if request.args.get("tickets_per_page"):
        tickets_limit += int(request.args.get("tickets_per_page"))
    location_name = request.args.get("location")
    categories = request.args.getlist("categories")
    tickets_query = m.Ticket.select()

    if search_query:
        tickets_query = tickets_query.where(
            m.Ticket.event.has(m.Event.name.ilike(f"%{search_query}%"))
        )

    if location_name:
        location_query = m.Location.select().where(m.Location.name == location_name)
        location = db.session.scalar(location_query)
        tickets_query = tickets_query.where(m.Ticket.event.has(location_id=location.id))

    if categories:
        tickets_query = (
            db.session.query(m.Ticket)
            .join(m.Event)
            .join(m.Category)
            .filter(m.Category.name.in_(categories))
        )

    if request.args.get("date_from"):
        tickets_query = tickets_query.where(
            m.Ticket.event.date_time >= request.args.get("date_from")
        )
    if request.args.get("date_to"):
        tickets_query = tickets_query.where(
            m.Ticket.event.date_time <= request.args.get("date_to")
        )

    tickets_query = tickets_query.limit(tickets_limit)

    categories = db.session.scalars(m.Category.select())
    locations = db.session.scalars(m.Location.select())
    tickets = db.session.scalars(tickets_query).all()

    if (
        request.args.get("q")
        or request.args.get("categories")
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
