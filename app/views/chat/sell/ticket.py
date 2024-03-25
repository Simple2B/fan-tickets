from flask import request, Blueprint, render_template
from flask_login import login_required
from psycopg2 import IntegrityError
from app import controllers as c
from app import forms as f
from app import models as m, db
from app.logger import log

from config import config

CFG = config()

ticket_blueprint = Blueprint("ticket", __name__, url_prefix="/ticket")


@ticket_blueprint.route("/get_quantity")
@login_required
def get_quantity():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.tickets_quantity_answer:
        log(log.INFO, "Tickets quantity answer: [%s]", params.tickets_quantity_answer)
        ticket = c.create_ticket(params, room)

        if params.tickets_quantity_answer == "2":
            return render_template(
                "chat/sell/ticket_separate_sell.html",
                ticket_unique_id=ticket.unique_id,
                room=room,
                now=c.utcnow_chat_format(),
                event_unique_id=params.event_unique_id,
            )
        types = [t.value.replace("_", " ").title() for t in m.TicketType]
        return render_template(
            "chat/sell/ticket_type.html",
            ticket_unique_id=ticket.unique_id,
            room=room,
            types=types,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    return render_template(
        "chat/sell/ticket_quantity.html",
        room=room,
        event_unique_id=params.event_unique_id,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/get_separate_sell")
@login_required
def get_separate_sell():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.ticket_paired is not None:
        log(log.INFO, "Tickets paired answer: [%s]", params.ticket_paired)
        user_message = (
            "No, this ticket has to be sold with the pair"
            if params.ticket_paired
            else "Yes, this ticket can be sold separately"
        )
        c.save_message(
            "Got it! Do you allow sell tickets separately? Choose or write below the answer",
            user_message,
            room,
        )

        ticket = c.create_paired_ticket(params, room)

        types = [t.value.replace("_", " ").title() for t in m.TicketType]
        return render_template(
            "chat/sell/ticket_type.html",
            ticket_unique_id=ticket.unique_id,
            room=room,
            types=types,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    return render_template(
        "chat/sell/ticket_separate_sell.html",
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/get_type")
@login_required
def get_type():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.ticket_type:
        log(log.ERROR, "No ticket type provided: [%s]", params.ticket_type)
        return render_template(
            "chat/sell/ticket_type.html",
            error_message="No ticket type provided, please, add ticket type",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.ticket_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add ticket details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    try:
        ticket.ticket_type = params.ticket_type.replace(" ", "_").lower()
        # TODO: paired ticket
        if ticket.is_paired:
            ticket2_query = m.Ticket.select().where(m.Ticket.unique_id == ticket.pair_unique_id)
            ticket2: m.Ticket = db.session.scalar(ticket2_query)
            ticket2.ticket_type = ticket.ticket_type
        ticket.save()
        log(log.INFO, "Ticket type added: [%s]", ticket.unique_id)
        c.save_message(
            "Got it! What is the type of ticket are you selling?",
            f"{params.ticket_type}",
            room,
        )
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Error commit: [%s]", e)
        return render_template(
            "chat/sell/ticket_type.html",
            error_message="Form submitting error. Please add your ticket type again",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    ticket_categories = [t.value.replace("_", " ").title() for t in m.TicketCategory]
    return render_template(
        "chat/sell/ticket_category.html",
        room=room,
        ticket_unique_id=ticket.unique_id,
        ticket_categories=ticket_categories,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/get_category")
@login_required
def get_category():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.ticket_category:
        log(log.ERROR, "No ticket category provided: [%s]", params.ticket_category)
        return render_template(
            "chat/sell/ticket_category.html",
            error_message="No ticket category provided, please, add ticket category",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    ticket = c.add_ticket_category(params, room)

    if not ticket:
        log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add ticket details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_has_section.html",
        room=room,
        event_unique_id=params.event_unique_id,
        ticket_unique_id=ticket.unique_id,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/get_notes")
@login_required
def get_notes():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.user_message == "" or params.user_message:
        ticket_modified = c.add_ticket_notes(params, room)
        log(log.INFO, "Ticket notes added: [%s]", ticket_modified.description)

        if not ticket_modified:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, input ticket details again",
                room=room,
                now=c.utcnow_chat_format(),
            )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    is_paired = ticket.is_paired if ticket else False
    return render_template(
        "chat/sell/ticket_price.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        ticket_paired=is_paired,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/get_price")
@login_required
def get_price():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.user_message:
        try:
            users_price = int(params.user_message)
        except ValueError as e:
            log(log.ERROR, "Invalid ticket price. Error: [%s], price: [%s]", e, params.user_message)
            return render_template(
                "chat/sell/ticket_price.html",
                error_message="Invalid ticket price, please enter a price in the format 100",
                room=room,
                now=c.utcnow_chat_format(),
                ticket_unique_id=params.ticket_unique_id,
            )
        ticket_modified = c.add_ticket_price(params, room, users_price)
        log(log.INFO, "Ticket's price is set: [%s]", ticket_modified.price_gross)

        if not ticket_modified:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, input ticket details again",
                room=room,
                now=c.utcnow_chat_format(),
            )
    else:
        log(log.ERROR, "No ticket price provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/ticket_price.html",
            error_message="No ticket price provided, please, add ticket price",
            ticket_unique_id=params.ticket_unique_id,
            event_unique_id=params.event_unique_id,
            room=room,
            now=c.utcnow_chat_format(),
        )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    ticket_unique_id = ticket.unique_id if ticket else params.ticket_unique_id
    return render_template(
        "chat/sell/ticket_details.html",
        ticket_unique_id=ticket_unique_id,
        ticket=ticket,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/get_details")
@login_required
def get_details():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    c.ticket_details(ticket, room)

    return render_template(
        "chat/sell/ticket_details.html",
        ticket_unique_id=params.ticket_unique_id,
        ticket=ticket,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/file_type")
@login_required
def get_file_type():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    c.ticket_details(ticket, room)

    if params.user_message == "PDF":
        log(log.INFO, "User choose PDF file type: [%s]", params.user_message)
        c.save_message("What version of ticket do you have?", "PDF", room)
        form: f.ChatFileUploadForm = f.ChatFileUploadForm()
        return render_template(
            "chat/sell/ticket_document.html",
            ticket_unique_id=params.ticket_unique_id,
            ticket_paired=ticket.is_paired,
            room=room,
            form=form,
            now=c.utcnow_chat_format(),
        )
    elif params.user_message == "wallet_id":
        log(log.INFO, "User choose wallet id file type: [%s]", params.user_message)
        c.save_message("What version of ticket do you have?", "Wallet id", room)
        return render_template(
            "chat/sell/ticket_wallet_id.html",
            ticket_unique_id=params.ticket_unique_id,
            ticket_paired=ticket.is_paired,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_file_type.html",
        ticket_unique_id=params.ticket_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/get_wallet_code")
@login_required
def get_wallet_code():
    params = c.validate_cell_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.user_message:
        ticket, is_second_wallet_id_input = c.add_ticket_wallet_id(params, room)
        log(log.INFO, "Tickets wallet id added: [%s]", ticket.wallet_id)

        if is_second_wallet_id_input:
            return render_template(
                "chat/sell/ticket_wallet_id.html",
                ticket_unique_id=ticket.pair_unique_id,
                ticket_paired=params.ticket_paired,
                is_second_wallet_id_input=is_second_wallet_id_input,
                room=room,
                now=c.utcnow_chat_format(),
            )

        if not ticket:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, input ticket details again",
                room=room,
                now=c.utcnow_chat_format(),
            )

        return render_template(
            "chat/sell/ticket_posted.html",
            ticket_unique_id=params.ticket_unique_id,
            event_unique_id=params.event_unique_id,
            ticket_paired=params.ticket_paired,
            room=room,
            now=c.utcnow_chat_format(),
        )
    return render_template(
        "chat/sell/ticket_wallet_id.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        ticket_paired=params.ticket_paired,
        room=room,
        now=c.utcnow_chat_format(),
    )


@ticket_blueprint.route("/get_ticket_document", methods=["GET", "POST"])
@login_required
def get_ticket_document():
    if request.method == "GET":
        params_input = request.args
    else:
        params_input = request.values

    params = c.validate_cell_ticket_params(params_input)

    room = c.get_room(params.room_unique_id)

    form: f.ChatFileUploadForm = f.ChatFileUploadForm()
    if form.validate_on_submit():
        files = request.files.getlist("file")
        if not c.check_file_type(files):
            return render_template(
                "chat/sell/ticket_document.html",
                error_message="Invalid file type. Please upload a PDF file",
                ticket_unique_id=params.ticket_unique_id,
                ticket_paired=params.ticket_paired,
                room=room,
                form=form,
                now=c.utcnow_chat_format(),
            )

        ticket_query = m.Ticket.select().where(m.Ticket.unique_id == params.ticket_unique_id)
        ticket: m.Ticket = db.session.scalar(ticket_query)

        if ticket.is_paired and len(files) != 2:
            return render_template(
                "chat/sell/ticket_document.html",
                error_message="Please upload TWO files",
                ticket_unique_id=params.ticket_unique_id,
                ticket_paired=ticket.is_paired,
                room=room,
                form=form,
                now=c.utcnow_chat_format(),
            )

        ticket_modified = c.add_ticket_document(params, files, ticket, room)
        log(log.INFO, "Tickets PDF document is added: [%s]", files)

        if not ticket_modified:
            log(log.ERROR, "Ticket not found: [%s]", params.event_unique_id)
            return render_template(
                "chat/sell/event_name.html",
                error_message="Something went wrong, please, input ticket details again",
                room=room,
                now=c.utcnow_chat_format(),
            )

        return render_template(
            "chat/sell/ticket_posted.html",
            ticket_unique_id=params.ticket_unique_id,
            event_unique_id=params.event_unique_id,
            ticket_paired=params.ticket_paired,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_document.html",
        ticket_unique_id=params.ticket_unique_id,
        event_unique_id=params.event_unique_id,
        ticket_paired=params.ticket_paired,
        room=room,
        form=form,
        now=c.utcnow_chat_format(),
    )
