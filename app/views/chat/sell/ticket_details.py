from flask import request, Blueprint, render_template
from flask_login import login_required
from app import controllers as c
from app import models as m, db
from app.logger import log

from config import config

CFG = config()

ticket_details_blueprint = Blueprint("ticket_details", __name__, url_prefix="/ticket_details")


@ticket_details_blueprint.route("/has_section")
@login_required
def has_section():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.ticket_has_section is False:
        c.save_message("Does this ticket have a section?", "Ticket does not have a section", room)
        log(log.ERROR, "Ticket has no section: [%s]", params.ticket_has_section)
        return render_template(
            "chat/sell/ticket_has_queue.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    c.save_message("Does this ticket have a section?", "Ticket has a section", room)
    log(log.ERROR, "Ticket has a section: [%s]", params.ticket_has_section)
    return render_template(
        "chat/sell/ticket_get_section.html",
        room=room,
        ticket_unique_id=params.ticket_unique_id,
        now=c.utcnow_chat_format(),
    )


@ticket_details_blueprint.route("/get_section")
@login_required
def get_section():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.user_message:
        ticket = c.add_ticket_section(params, room)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, add event name",
                room=room,
                now=c.utcnow_chat_format(),
            )

        return render_template(
            "chat/sell/ticket_has_queue.html",
            ticket_unique_id=params.ticket_unique_id,
            event_unique_id=params.event_unique_id,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_get_section.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_details_blueprint.route("/has_queue")
@login_required
def has_queue():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.ticket_has_queue is False:
        c.save_message("Does this ticket have a queue?", "Ticket does not have a queue", room)
        log(log.ERROR, "Ticket has no queue: [%s]", params.ticket_has_queue)
        return render_template(
            "chat/sell/ticket_has_seat.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    c.save_message("Does this ticket have a queue?", "Ticket has a queue", room)
    log(log.INFO, "Ticket has a queue: [%s]", params.user_message)
    return render_template(
        "chat/sell/ticket_get_queue.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_details_blueprint.route("/get_queue")
@login_required
def get_queue():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.user_message:
        ticket = c.add_ticket_queue(params, room)
        log(log.INFO, "Ticket queue added: [%s]", ticket.queue)

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, add event name",
                room=room,
                now=c.utcnow_chat_format(),
            )

    return render_template(
        "chat/sell/ticket_has_seat.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_details_blueprint.route("/has_seat")
@login_required
def has_seat():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.ticket_has_seat:
        c.save_message("Does this ticket have a seat?", "Ticket does not have a seat", room)
        log(log.ERROR, "Ticket has no seat: [%s]", params.ticket_has_seat)
        return render_template(
            "chat/sell/ticket_notes.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    c.save_message("Does this ticket have a seat?", "Ticket has a seat", room)
    log(log.INFO, "Ticket has a seat: [%s]", params.ticket_has_seat)

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    return render_template(
        "chat/sell/ticket_get_seat.html",
        ticket_unique_id=params.ticket_unique_id,
        ticket_paired=ticket.is_paired,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_details_blueprint.route("/get_seat")
@login_required
def get_seat():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.user_message:
        ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
        ticket: m.Ticket = db.session.scalar(ticket_query)

        if ticket.is_paired and "," not in params.user_message:
            return render_template(
                "chat/sell/ticket_get_seat.html",
                error_message="Please enter seats for both tickets separating them with comma",
                ticket_unique_id=params.ticket_unique_id,
                ticket_paired=ticket.is_paired,
                event_unique_id=params.event_unique_id,
                room=room,
                now=c.utcnow_chat_format(),
            )

        ticket_modified = c.add_ticket_seat(params, room)
        log(log.INFO, "Ticket seat added: [%s]", ticket_modified.seat)

        if not ticket_modified:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, add event name",
                room=room,
                now=c.utcnow_chat_format(),
            )

    return render_template(
        "chat/sell/ticket_notes.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )
