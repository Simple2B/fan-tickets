from datetime import datetime, timedelta
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db
from app.logger import log
from config import config

CFG = config()

chat_sell_blueprint = Blueprint("sell", __name__, url_prefix="/sell")


@chat_sell_blueprint.route("/", methods=["GET", "POST"])
@login_required
def get_events():
    # TODO: add timezone
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    location_input = request.args.get("event_location")
    date_input = request.args.get("event_date")

    room = m.Room(
        seller_id=current_user.id,
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
            "chat/sell/00_event_init.html",
            locations=m.Location.all(),
            error_message=error_message,
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=current_user.id,
        room_id=room.id,
        text=f"location: {location_input}\ndate: {date_input}",
    ).save(False)

    location = db.session.scalar(m.Location.select().where(m.Location.name == location_input))
    # TODO: add logic that creates a new location in case there is no such location in the database

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
            "chat/sell/02_event_create.html",
            error_message="There is no such events in our database. Let's create a new one!",
            event_location=location_input,
            event_date=date_input,
            room=room,
            now=now_str,
            user=current_user,
        )

    db.session.commit()

    return render_template(
        "chat/sell/02_events_list.html",
        now=now_str,
        room=room,
        events=events,
        event_location=location_input,
        event_date=date_input,
    )


@chat_sell_blueprint.route("/get_event_name")
@login_required
def get_event_name():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.event_name:
        log(log.ERROR, "No event date provided: [%s]", params.event_name)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="No event date provided",
            room=room,
            now=response.now_str,
        )

    assert room
    c.send_message(
        "Please, input official event name (matching the official website)",
        f"Event name: {params.event_name}",
        room,
    )

    return render_template(
        "chat/sell/02_event_location.html",
        event_name=params.event_name,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_event_location")
@login_required
def get_event_location():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.event_name:
        log(log.ERROR, "No event date provided: [%s]", params.event_name)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    if not params.event_location:
        log(log.ERROR, "No event location provided: [%s]", params.event_location)
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="No event location provided, please, add event location",
            room=room,
            now=response.now_str,
        )

    assert room
    c.send_message(
        "Please, input event location",
        f"Event location: {params.event_location}",
        room,
    )

    return render_template(
        "chat/sell/03_event_date.html",
        event_location=params.event_location,
        event_name=params.event_name,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_event_date")
@login_required
def get_event_date():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.event_name:
        log(log.ERROR, "No event date provided: [%s]", params.event_name)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    if not params.event_location:
        log(log.ERROR, "No event location provided: [%s]", params.event_location)
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Something went wrong, please, add event location",
            room=room,
            now=response.now_str,
        )

    if not params.event_date:
        log(log.ERROR, "No event date provided: [%s]", params.event_date)
        return render_template(
            "chat/sell/03_event_date.html",
            error_message="No event date provided, please, add event date",
            room=room,
            now=response.now_str,
        )

    assert room
    c.send_message(
        "Please, input event date",
        f"Event date: {params.event_date}",
        room,
    )

    return render_template(
        "chat/sell/04_event_time.html",
        event_date=params.event_date,
        event_location=params.event_location,
        event_name=params.event_name,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_event_time")
@login_required
def get_event_time():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.event_name:
        log(log.ERROR, "No event date provided: [%s]", params.event_name)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    if not params.event_location:
        log(log.ERROR, "No event location provided: [%s]", params.event_location)
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Something went wrong, please, add event location",
            room=room,
            now=response.now_str,
        )

    if not params.event_date:
        log(log.ERROR, "No event date provided: [%s]", params.event_date)
        return render_template(
            "chat/sell/03_event_date.html",
            error_message="Something went wrong, please, add event date",
            room=room,
            now=response.now_str,
        )

    if not params.event_time:
        log(log.ERROR, "No event time provided: [%s]", params.event_time)
        return render_template(
            "chat/sell/04_event_time.html",
            error_message="No event time provided, please, add event time",
            room=room,
            now=response.now_str,
        )

    assert room
    c.send_message(
        "Please, input event time",
        f"Event time: {params.event_time}",
        room,
    )

    return render_template(
        "chat/sell/04_event_time.html",
        event_date=params.event_date,
        get_event_time=params.event_time,
        event_location=params.event_location,
        event_name=params.event_name,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_event_category")
@login_required
def get_event_category():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.event_name:
        log(log.ERROR, "No event date provided: [%s]", params.event_name)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    if not params.event_location:
        log(log.ERROR, "No event location provided: [%s]", params.event_location)
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Something went wrong, please, add event location",
            room=room,
            now=response.now_str,
        )

    if not params.event_date:
        log(log.ERROR, "No event date provided: [%s]", params.event_date)
        return render_template(
            "chat/sell/03_event_date.html",
            error_message="Something went wrong, please, add event date",
            room=room,
            now=response.now_str,
        )

    if not params.event_time:
        log(log.ERROR, "No event time provided: [%s]", params.event_time)
        return render_template(
            "chat/sell/04_event_time.html",
            error_message="Something went wrong, please, add event time",
            room=room,
            now=response.now_str,
        )

    if not params.event_category:
        log(log.ERROR, "No event type provided: [%s]", params.event_category)
        return render_template(
            "chat/sell/05_event_category.html",
            error_message="No event type provided, please, add event type",
            room=room,
            now=response.now_str,
        )

    assert room
    event = c.create_event(params, room)

    return render_template(
        "chat/sell/06_ticket_type.html",
        event_unique_id=event.unique_id,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_ticket_type")
@login_required
def get_ticket_type():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.event_unique_id:
        log(log.ERROR, "Not found event_unique_id: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    if not params.ticket_type:
        log(log.ERROR, "No ticket type provided: [%s]", params.ticket_type)
        return render_template(
            "chat/sell/06_ticket_type.html",
            error_message="No ticket type provided, please, add ticket type",
            room=room,
            now=response.now_str,
        )

    assert room
    ticket = c.create_ticket(params, room)

    if not ticket:
        log(log.ERROR, "Event not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    return render_template(
        "chat/sell/07_ticket_category.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_ticket_category")
@login_required
def get_ticket_category():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/02_event_location.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.ticket_unique_id:
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    if not params.ticket_category:
        log(log.ERROR, "No ticket category provided: [%s]", params.ticket_category)
        return render_template(
            "chat/sell/07_ticket_category.html",
            error_message="No ticket category provided, please, add ticket category",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    assert room
    ticket = c.add_ticket_category(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    return render_template(
        "chat/sell/08_ticket_section.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_ticket_section")
@login_required
def get_ticket_section():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.ticket_unique_id:
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    assert room

    if not params.ticket_has_section:
        c.send_message("Does this ticket have a section?", "Ticket has no a section", room)
        log(log.ERROR, "Ticket has no section: [%s]", params.ticket_has_section)
        return render_template(
            "chat/sell/09_ticket_queue.html",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.ticket_section:
        log(log.ERROR, "No ticket section provided: [%s]", params.ticket_section)
        return render_template(
            "chat/sell/08_ticket_section.html",
            error_message="No ticket section provided, please, add ticket section or choose 'No section'",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    ticket = c.add_ticket_section(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    return render_template(
        "chat/sell/09_ticket_queue.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_ticket_queue")
@login_required
def get_ticket_queue():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.ticket_unique_id:
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    assert room

    if not params.ticket_has_queue:
        c.send_message("Does this ticket have a queue?", "Ticket has no a queue", room)
        log(log.ERROR, "Ticket has no queue: [%s]", params.ticket_has_queue)
        return render_template(
            "chat/sell/10_ticket_seat.html",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.ticket_queue:
        log(log.ERROR, "No ticket queue provided: [%s]", params.ticket_queue)
        return render_template(
            "chat/sell/09_ticket_queue.html",
            error_message="No ticket queue provided, please, add ticket queue or choose 'No queue'",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    ticket = c.add_ticket_queue(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    return render_template(
        "chat/sell/10_ticket_seat.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_ticket_seat")
@login_required
def get_ticket_seat():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.ticket_unique_id:
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    assert room

    if not params.ticket_has_seat:
        c.send_message("Does this ticket have a seat?", "Ticket has no seat", room)
        log(log.ERROR, "Ticket has no seat: [%s]", params.ticket_has_seat)
        return render_template(
            "chat/sell/11_ticket_notes.html",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.ticket_seat:
        log(log.ERROR, "No ticket seat provided: [%s]", params.ticket_seat)
        return render_template(
            "chat/sell/10_ticket_seat.html",
            error_message="No ticket seat provided, please, add ticket seat or choose 'No seat'",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    ticket = c.add_ticket_seat(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    return render_template(
        "chat/sell/11_ticket_notes.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_ticket_notes")
@login_required
def get_ticket_notes():
    params = s.ChatSellParams.model_validate(dict(request.args))

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.ticket_unique_id:
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    assert room

    if not params.ticket_has_notes:
        c.send_message("Do you want to add notes?", "Without notes", room)
        log(log.ERROR, "Ticket without notes: [%s]", params.ticket_has_notes)
        return render_template(
            "chat/sell/12_ticket_document.html",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.ticket_notes:
        log(log.ERROR, "No ticket notes provided: [%s]", params.ticket_notes)
        return render_template(
            "chat/sell/11_ticket_notes.html",
            error_message="No ticket notes provided, please, add ticket notes or choose 'Without notes'",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    ticket = c.add_ticket_notes(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    return render_template(
        "chat/sell/12_ticket_document.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/get_ticket_document")
@login_required
def get_ticket_document():
    form: f.ChatTicketDocumentForm = f.ChatTicketDocumentForm()

    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == form.room_unique_id.data)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found: [%s]", form.room_unique_id.data)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error, room_unique_id: [%s]",
            form.room_unique_id.data,
        )
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
        )

    if not form.file.data:
        log(log.ERROR, "No ticket document: [%s]", form.file.data)
        return render_template(
            "chat/sell/12_ticket_document.html",
            error_message="No ticket document, please upload your ticket document",
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    error_message = c.add_ticket_document(form, room)

    if error_message:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/04_identification.html",
            error_message=error_message,
            room=room,
            now=now_str,
            user_unique_id=form.user_unique_id.data,
        )

    return render_template(
        "chat/registration/05_name.html",
        room=room,
        now=now_str,
        user_unique_id=form.user_unique_id.data,
    )

    response, room = c.check_room_id(params)

    if response.is_error:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        # TODO: what if we return user to start of the chat?
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Form submitting error",
            room=room,
            now=response.now_str,
        )

    if not params.ticket_unique_id:
        log(log.ERROR, "Not found ticket_unique_id: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    assert room

    if not params.ticket_has_notes:
        c.send_message("Do you want to add notes?", "Without notes", room)
        log(log.ERROR, "Ticket without notes: [%s]", params.ticket_has_notes)
        return render_template(
            "chat/sell/12_ticket_document.html",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.ticket_notes:
        log(log.ERROR, "No ticket notes provided: [%s]", params.ticket_notes)
        return render_template(
            "chat/sell/11_ticket_notes.html",
            error_message="No ticket notes provided, please, add ticket notes or choose 'Without notes'",
            room=room,
            now=response.now_str,
            ticket_unique_id=params.ticket_unique_id,
        )

    ticket = c.add_ticket_notes(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/01_event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=response.now_str,
        )

    return render_template(
        "chat/sell/12_ticket_document.html",
        ticket_unique_id=ticket.unique_id,
        room=room,
        now=response.now_str,
    )


@chat_sell_blueprint.route("/event_form", methods=["GET", "POST"])
@login_required
def event_form():
    event_location = request.args.get("event_location")
    event_date = request.args.get("event_date")
    room_unique_id = request.args.get("room_unique_id")

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    error_message = ""
    if not event_location:
        log(log.ERROR, "No event location provided: [%s]", event_location)
        error_message += "No event location provided\n"
    if not event_date:
        log(log.ERROR, "No event date provided: [%s]", event_date)
        error_message += "No event date provided\n"

    if error_message:
        return render_template(
            "chat/sell/02_event_create.html",
            error_message=error_message,
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="No events found. Let's create a new one!",
    ).save(False)

    return render_template(
        "chat/sell/02_event_create.html",
        event_location=event_location,
        event_date=event_date,
        room=room,
        now=now_str,
        user=current_user,
    )


@chat_sell_blueprint.route("/create_event", methods=["GET", "POST"])
@login_required
def create_event():
    event_name = request.args.get("event_name")
    event_location = request.args.get("event_location")
    event_category = request.args.get("event_category")
    event_date = request.args.get("event_date")
    event_url = request.args.get("event_url")
    room_unique_id = request.args.get("room_unique_id")

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    error_message = ""

    if not event_name:
        log(log.ERROR, "No event name provided: [%s]", event_name)
        error_message += "No event name provided \n"
    if not event_location:
        log(log.ERROR, "No event location provided: [%s]", event_location)
        error_message += "No event location provided \n"
    if not event_category:
        log(log.ERROR, "No event category provided: [%s]", event_category)
        error_message += "No event category provided \n"
    if not event_date:
        log(log.ERROR, "No event date provided: [%s]", event_date)
        error_message += "No event date provided \n"
    if not event_url:
        log(log.ERROR, "No event url provided: [%s]", event_url)
        error_message += "No event url provided \n"

    if error_message:
        return render_template(
            "chat/sell/02_event_create.html",
            error_message=error_message,
            room=room,
            now=now_str,
            user=current_user,
        )

    # TODO: what should we do if there is no such location or category?
    location_query = m.Location.select().where(m.Location.name == event_location)
    location = db.session.scalar(location_query)
    if not location:
        log(log.ERROR, "Location not found: [%s]", event_location)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Location not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    category_query = m.Category.select().where(m.Category.name == event_category)
    category = db.session.scalar(category_query)
    if not category:
        log(log.ERROR, "Category not found: [%s]", event_category)
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Category not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    if not event_date:
        return render_template(
            "chat/sell/02_event_create.html",
            error_message="Event date not found",
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="There is no such events in our database. Let's create a new one!",
    ).save(False)
    m.Message(
        sender_id=current_user.id,
        room_id=room.id,
        text=f"{event_name}\n {event_location}\n {event_category}\n {event_date}\n {event_url}",
    ).save(False)

    event = m.Event(
        name=event_name,
        location=location,
        category=category,
        date_time=datetime.strptime(event_date, app.config["DATE_PICKER_FORMAT"]),
        url=event_url,
        creator_id=current_user.id,
    ).save()
    log(log.INFO, "Event created: [%s]", event)

    # TODO: check with Bard if events exist

    return render_template(
        "chat/sell/03_ticket_create.html",
        event=event,
        room=room,
        now=now_str,
        user=current_user,
    )


@chat_sell_blueprint.route("/ticket_form", methods=["GET", "POST"])
@login_required
def ticket_form():
    room_unique_id = request.args.get("room_unique_id")
    event_id = request.args.get("event_id")

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/03_ticket_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Please, input ticket details.",
    ).save(False)

    # TODO: check with Bard if events exist
    event = db.session.scalar(m.Event.select().where(m.Event.unique_id == event_id))

    return render_template(
        "chat/sell/03_ticket_create.html",
        event=event,
        room=room,
        now=now_str,
        user=current_user,
    )


@chat_sell_blueprint.route("/create_ticket", methods=["GET", "POST"])
@login_required
def create_ticket():
    section = request.args.get("section")
    queue = request.args.get("queue")
    seat = request.args.get("seat")
    quantity = request.args.get("quantity")
    price = request.args.get("price")
    room_unique_id = request.args.get("room_unique_id")
    event_id = request.args.get("event_id")
    # TODO: add file input for ticket

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")

    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)
        return render_template(
            "chat/sell/03_ticket_create.html",
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user=current_user,
        )

    error_message = ""

    if not section:
        log(log.ERROR, "No section provided: [%s]", section)
        error_message += "No section provided \n"
    if not queue:
        log(log.ERROR, "No queue provided: [%s]", queue)
        error_message += "No queue provided \n"
    if not seat:
        log(log.ERROR, "No seat provided: [%s]", seat)
        error_message += "No seat provided \n"
    if not quantity:
        log(log.ERROR, "No quantity provided: [%s]", quantity)
        error_message += "No quantity provided \n"
    if not price:
        log(log.ERROR, "No price provided: [%s]", price)
        error_message += "No price provided \n"

    event = db.session.scalar(m.Event.select().where(m.Event.unique_id == event_id))
    if not event:
        log(log.ERROR, "Event not found: [%s]", event_id)
        return render_template(
            "chat/sell/03_ticket_create.html",
            error_message="Event not found",
            event=event,
            room=room,
            now=now_str,
            user=current_user,
        )

    if error_message:
        return render_template(
            "chat/sell/03_ticket_create.html",
            error_message=error_message,
            event=event,
            room=room,
            now=now_str,
            user=current_user,
        )

    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="There is no such events in our database. Let's create a new one!",
    ).save(False)
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text="Event has been successfully added!",
    ).save(False)
    m.Message(
        sender_id=current_user.id,
        room_id=room.id,
        text=f"section: {section}\nqueue:{queue}\nseat:{seat}\nquantity:{quantity}\nprice:{price}",
    ).save(False)

    if price:
        price_gross = float(price) * app.config["PLATFORM_COMMISSION_RATE"]
        log(log.INFO, "Commission applied: [%s]", price_gross)

    ticket = m.Ticket(
        event=event,
        section=section,
        queue=queue,
        seat=seat,
        quantity=quantity,
        price_net=price,
        price_gross=price_gross,
        seller_id=current_user.id,
    ).save()

    return render_template(
        "chat/sell/04_ticket_success.html",
        ticket=ticket,
        room=room,
        now=now_str,
        user=current_user,
    )
