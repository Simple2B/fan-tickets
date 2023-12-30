from datetime import datetime, timedelta
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from flask_mail import Message

import sqlalchemy as sa

from app import controllers as c
from app import schema as s
from app import models as m, db, mail
from app.logger import log
from config import config

CFG = config()

chat_buy_blueprint = Blueprint("buy", __name__, url_prefix="/buy")


@chat_buy_blueprint.route("/get_event_name", methods=["GET", "POST"])
@login_required
def get_event_name():
    try:
        params = s.ChatBuyEventParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if params.renew_search:
        log(log.ERROR, "Renew search")
        return render_template(
            "chat/buy/event_name.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No event name provided: [%s]", params.user_message)
        return render_template(
            "chat/buy/event_name.html",
            error_message="No event date provided. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    events = c.get_event_by_name(params.user_message, room)

    if not events:
        log(log.INFO, "Events not found: [%s]", params.user_message)
        return render_template(
            "chat/buy/ticket_not_found.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    first_event: m.Event = events[0]
    if len(events) == 1:
        log(log.INFO, "Only 1 event found: [%s]", params.user_message)

        tickets = c.get_tickets_by_event(first_event, room)
        if not tickets:
            log(log.ERROR, "Tickets not found: [%s]", params.user_message)
            return render_template(
                "chat/buy/ticket_not_found.html",
                room=room,
                now=c.utcnow_chat_format(),
            )

        log(log.INFO, "Tickets found: [%s]", tickets)
        return render_template(
            "chat/buy/ticket_list.html",
            event_id=first_event.unique_id,
            room=room,
            now=c.utcnow_chat_format(),
            tickets=tickets,
        )

    locations = c.get_locations_by_events(events, room)
    if not locations:
        log(log.ERROR, "Locations not found: [%s]", params.user_message)
        return render_template(
            "chat/buy/ticket_not_found.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if len(locations) == 1:
        log(log.INFO, "Only 1 location found: [%s]", params.user_message)
        return render_template(
            "chat/buy/ticket_date.html",
            events=events,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/buy/location_list.html",
        event_unique_id=first_event.unique_id,
        locations=locations,
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_buy_blueprint.route("/", methods=["GET", "POST"])
def get_events():
    # TODO: add timezone
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    location_input = request.args.get("event_location")
    date_input = request.args.get("event_date")
    event_name_input = request.args.get("event_name")

    room = m.Room(
        seller_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="What event are you selling tickets for?",
    ).save(False)
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please, input location and date or search by event name.",
    ).save(False)

    error_message = ""

    if not location_input and not event_name_input:
        log(log.ERROR, "No event location provided: [%s]", location_input)
        error_message += "No event location provided \n"

    if not date_input and not event_name_input:
        log(log.ERROR, "No event date provided: [%s]", date_input)
        error_message += "No event date provided \n"

    if not event_name_input and not location_input and not date_input:
        log(log.ERROR, "Please, enter location and date or event name: [%s]", event_name_input)
        error_message += "Please, enter location and date or event name \n"

    if error_message:
        return render_template(
            "chat/buy/events_01_filters.html",
            locations=m.Location.all(),
            error_message=error_message,
            room=room,
            now=now_str,
            user=current_user,
        )

    text = ""
    if location_input and date_input:
        location = db.session.scalar(m.Location.select().where(m.Location.name == location_input))

        event_start_date = datetime.strptime(str(date_input), app.config["DATE_PICKER_FORMAT"])
        event_end_date = event_start_date + timedelta(days=1)

        events_query = m.Event.select().where(
            m.Event.location == location,
            m.Event.date_time >= event_start_date,
            m.Event.date_time <= event_end_date,
        )
        text = f"location: {location_input}\ndate: {date_input}"

    if event_name_input:
        events_query = m.Event.select().where(m.Event.name.ilike(f"%{event_name_input}%"))
        text = f"search query: {event_name_input}"

    m.Message(
        room_id=room.id,
        text=text,
    ).save(False)

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

    buyer_id = current_user.id if current_user.is_authenticated else None
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Choose an event from the list.",
    ).save(False)
    m.Message(
        sender_id=buyer_id,
        room_id=room.id,
        text=f"{event.name}",
    ).save()

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
    event: m.Event = db.session.scalar(event_query)

    if not event:
        log(log.ERROR, "Event not found: [%s]", event_unique_id)
        return render_template(
            "chat/buy/events_03_details.html",
            error_message="Event not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    buyer_id = current_user.id if current_user.is_authenticated else None
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=f"Event details:\n{event.name}\n{event.date_time.strftime(app.config['DATE_PLATFORM_FORMAT'])}\n{event.location.name}",
    ).save(False)

    m.Message(
        sender_id=buyer_id,
        room_id=room.id,
        text=f"Give me please tickets for this event: {event.name}",
    ).save(False)
    db.session.commit()

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

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=f"Ticket details:\n{event.name}\n{event.date_time.strftime(app.config['DATE_PLATFORM_FORMAT'])}\n{event.location.name}",
    ).save(False)
    db.session.commit()

    return render_template(
        "chat/buy/tickets_05_details.html",
        now=now_str,
        room=room,
        event=event,
        ticket=ticket,
    )


def compute_total_price(cart_tickets: list[m.Ticket]) -> float:
    return sum([ticket.price_gross for ticket in cart_tickets])


def clear_message_history(room: m.Room) -> None:
    if not room:
        log(log.ERROR, "Room not found: [%s]", room)
        return

    messages_query = m.Message.select().where(m.Message.room_id == room.id)
    messages = db.session.scalars(messages_query).all()

    msg = Message(
        subject=f"Today's chat history {datetime.now().strftime(app.config['DATE_CHAT_HISTORY_FORMAT'])}",
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[current_user.email],
    )
    msg.html = render_template(
        "email/chat_history.htm",
        user=current_user,
        messages=messages,
    )
    mail.send(msg)

    for message in messages:
        db.session.delete(message)
    db.session.commit()
    return


@chat_buy_blueprint.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    ticket_unique_id = request.args.get("ticket_unique_id")
    ticket_to_exclude = request.args.get("ticket_to_exclude")
    cart_from_navbar = request.args.get("cart_from_navbar")
    room_unique_id = request.args.get("room_unique_id")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    cart_tickets_query = m.Ticket.select().where(m.Ticket.buyer == current_user)

    if cart_from_navbar:
        if room:
            clear_message_history(room)
        cart_tickets = db.session.scalars(cart_tickets_query).all()
        total_price = compute_total_price(cart_tickets)
        log(log.INFO, "Cart opened from navbar")
        return render_template(
            "chat/buy/tickets_06_cart.html",
            cart_tickets=cart_tickets,
            total_price=total_price,
            now=now_str,
        )

    clear_message_history(room)

    if ticket_to_exclude:
        all_tickets = db.session.scalars(cart_tickets_query).all()
        cart_tickets = [ticket for ticket in all_tickets if ticket.unique_id != ticket_to_exclude]
        total_price = compute_total_price(cart_tickets)
        ticket_excluded: m.Ticket = db.session.scalar(m.Ticket.select().where(m.Ticket.unique_id == ticket_to_exclude))

        if not ticket_excluded:
            log(log.ERROR, "Ticket not found: [%s]", ticket_to_exclude)
            return render_template(
                "chat/buy/tickets_06_cart.html",
                cart_tickets=cart_tickets,
                total_price=total_price,
                now=now_str,
            )
        ticket_excluded.is_in_cart = False
        ticket_excluded.buyer_id = None
        db.session.commit()

        log(log.INFO, "Ticket removed from cart: [%s]", ticket_to_exclude)
        return render_template(
            "chat/buy/tickets_06_cart.html",
            cart_tickets=cart_tickets,
            total_price=total_price,
            now=now_str,
        )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    if not ticket:
        event_unique_id = request.args.get("event_unique_id")
        event = db.session.scalar(m.Event.select().where(m.Event.unique_id == event_unique_id))
        log(log.ERROR, "Ticket not found: [%s]", ticket_unique_id)
        return render_template(
            "chat/buy/events_04_tickets.html",
            error_message="Ticket not found",
            now=now_str,
            room=room,
            event=event,
            user=current_user,
        )
    ticket.is_in_cart = True
    ticket.buyer_id = current_user.id
    ticket.save()

    cart_tickets = db.session.scalars(cart_tickets_query).all()
    total_price = compute_total_price(cart_tickets)
    return render_template(
        "chat/buy/tickets_06_cart.html",
        cart_tickets=cart_tickets,
        total_price=total_price,
        room=room,
        now=now_str,
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
