from flask import request, Blueprint, render_template
from app import models as m, db


tickets_blueprint = Blueprint("tickets", __name__, url_prefix="/tickets")


@tickets_blueprint.route("/", methods=["GET", "POST"])
def get_tickets():
    location_name = request.args.get("location")
    if location_name:
        location_query = m.Location.select().where(m.Location.name == location_name)
        location = db.session.scalar(location_query)

    tickets_query = m.Event.select()

    if location_name:
        tickets_query = tickets_query.where(m.Ticket.event.has(location_id=location.id))

    tickets = db.session.scalars(tickets_query).all()
    return render_template("tickets/tickets.html", tickets=tickets)
