from datetime import datetime, timedelta
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from app import models as m, db
from app.logger import log
from config import config

CFG = config()

chat_buy_blueprint = Blueprint("buy", __name__, url_prefix="/buy")


@chat_buy_blueprint.route("/", methods=["GET", "POST"])
def get_events():
    # TODO: add timezone
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    location_input = request.args.get("event_location")
    date_input = request.args.get("event_date")

    room = m.Room(
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="What event are you selling tickets for?",
    ).save(False)
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please, input location and date.",
    ).save(False)

    error_message = ""

    if not location_input:
        log(log.ERROR, "No event location provided: [%s]", location_input)
        error_message += "No event location provided \n"

    if not date_input:
        log(log.ERROR, "No event date provided: [%s]", date_input)
        error_message += "No event date provided \n"

    if error_message:
        return render_template(
            "chat/buy/events_01_filters.html",
            locations=m.Location.all(),
            error_message=error_message,
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        room_id=room.id,
        text=f"{location_input}\n{date_input}",
    ).save(False)

    location = db.session.scalar(m.Location.select().where(m.Location.name == location_input))

    event_start_date = datetime.strptime(str(date_input), app.config["DATE_PICKER_FORMAT"])
    event_end_date = event_start_date + timedelta(days=1)
    events_query = m.Event.select().where(
        m.Event.location == location,
        m.Event.date_time >= event_start_date,
        m.Event.date_time <= event_end_date,
    )
    events = db.session.scalars(events_query).all()

    if not events:
        log(log.INFO, "No events found: [%s]", events)
        return render_template(
            "chat/buy/events_02_list.html",
            error_message="No events found",
            event_location=location_input,
            event_date=date_input,
            room=room,
            now=now_str,
            user=current_user,
        )

    db.session.commit()

    return render_template(
        "chat/buy/events_02_list.html",
        now=now_str,
        room=room,
        events=events,
        event_location=location_input,
        event_date=date_input,
    )


@chat_buy_blueprint.route("/event", methods=["GET", "POST"])
def event_details():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    event_unique_id = request.args.get("event_unique_id")
    room_unique_id = request.args.get("room_unique_id")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/buy/events_02_list.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    event_query = m.Event.select().where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.ERROR, "Event not found: [%s]", event_unique_id)
        return render_template(
            "chat/buy/events_02_list.html",
            error_message="Event not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    return render_template(
        "chat/buy/events_03_details.html",
        now=now_str,
        room=room,
        event=event,
    )


@chat_buy_blueprint.route("/event_tickets", methods=["GET", "POST"])
def get_event_tickets():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    event_unique_id = request.args.get("event_unique_id")
    room_unique_id = request.args.get("room_unique_id")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/buy/events_03_details.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    event_query = m.Event.select().where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)

    if not event:
        log(log.ERROR, "Event not found: [%s]", event_unique_id)
        return render_template(
            "chat/buy/events_03_details.html",
            error_message="Event not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        room_id=room.id,
        text=f"Give me please tickets for this event: {event.name}",
    ).save(False)

    return render_template(
        "chat/buy/events_04_tickets.html",
        now=now_str,
        room=room,
        event=event,
    )


@chat_buy_blueprint.route("/ticket_details", methods=["GET", "POST"])
def ticket_details():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    event_unique_id = request.args.get("event_unique_id")
    ticket_unique_id = request.args.get("ticket_unique_id")
    room_unique_id = request.args.get("room_unique_id")
    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/buy/events_04_tickets.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    event_query = m.Event.select().where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket = db.session.scalar(ticket_query)

    return render_template(
        "chat/buy/tickets_05_details.html",
        now=now_str,
        room=room,
        event=event,
        ticket=ticket,
    )


@chat_buy_blueprint.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room_unique_id = request.args.get("room_unique_id")
    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    ticket_unique_id = request.args.get("ticket_unique_id")
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/buy/events_04_tickets.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", ticket_unique_id)
        return render_template(
            "chat/buy/events_04_tickets.html",
            error_message="Ticket not found",
            room=room,
            now=now_str,
            user=current_user,
        )
    ticket.is_in_cart = True
    ticket.buyer_id = current_user.id
    ticket.save()

    cart_tickets_query = m.Ticket.select().where(m.Ticket.buyer == current_user)
    cart_tickets = db.session.scalars(cart_tickets_query).all()
    total_price = sum([ticket.price_gross for ticket in cart_tickets])
    return render_template(
        "chat/buy/tickets_06_cart.html",
        room=room,
        cart_tickets=cart_tickets,
        total_price=total_price,
    )


@chat_buy_blueprint.route("/pagar", methods=["GET", "POST"])
def pagar():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    event_unique_id = request.args.get("event_unique_id")
    ticket_unique_id = request.args.get("ticket_unique_id")
    room_unique_id = request.args.get("room_unique_id")
    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/buy/events_04_tickets.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )
    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket = db.session.scalar(ticket_query)
    event_query = m.Event.select().where(m.Event.unique_id == event_unique_id)
    event = db.session.scalar(event_query)
    return render_template(
        "chat/buy/tickets_07_pagar.html",
        room=room,
        event=event,
        ticket=ticket,
    )
