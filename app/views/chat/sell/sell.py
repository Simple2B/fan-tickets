from datetime import datetime
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from app import controllers as c
from app import models as m, db
from app.logger import log
from app.controllers.jinja_globals import transactions_last_month, transactions_per_event

from config import config

CFG = config()

sell_blueprint = Blueprint("sell", __name__, url_prefix="/sell")


@sell_blueprint.route("/get_event_category")
@login_required
def get_event_category():
    params = c.validate_event_sell_params(request.args)

    room = c.get_room(params.room_unique_id)

    global_fee_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
    if transactions_last_month(current_user) > global_fee_settings.selling_limit:
        return render_template(
            "chat/buy/transactions_limit.html",
            error_message="You have reached the limit of transactions per month",
            now=c.utcnow_chat_format(),
            room=room,
            selling=True,
        )

    category_name = db.session.scalar(
        m.Category.select()
        .where(m.Category.unique_id == params.event_category_id, m.Category.deleted.is_(False))
        .with_only_columns(m.Category.name)
    )

    if not category_name:
        category_name = "Other"

    c.save_message(
        "Great! What is the category of event are you selling tickets for?",
        f"{category_name}",
        room,
    )

    log(log.INFO, "Event category: [%s]", params.event_category_id)
    return render_template(
        "chat/sell/event_name.html",
        event_category_id=params.event_category_id if params.event_category_id else category_name,
        room=room,
        now=c.utcnow_chat_format(),
    )


@sell_blueprint.route("/get_event_name")
@login_required
def get_event_name():
    params = c.validate_event_sell_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.user_message:
        log(log.ERROR, "No event name provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_name.html",
            error_message="No event name provided. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
            event_category_id=params.event_category_id,
        )

    events = c.get_event_by_name_bard(params, room)

    if events:
        return render_template(
            "chat/sell/event_approve.html",
            event_name=params.user_message,
            events=events,
            event_category_id=params.event_category_id,
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/event_url.html",
        event_name=params.user_message,
        event_category_id=params.event_category_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@sell_blueprint.route("/event_approve")
@login_required
def event_approve():
    params = c.validate_event_sell_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.event_unique_id:
        event: m.Event = c.get_event_by_uuid(params.event_unique_id, room)
        if transactions_per_event(current_user, event) >= 2:
            c.save_message(
                "Unfortunately in order to avoid frauds we have to limit transactions. You can't perform more than 2 transactions per event.",
                f"Transactions per event: {transactions_per_event(current_user, event)}",
                room,
            )
            return render_template(
                "chat/buy/transactions_limit.html",
                error_message="You have reached the limit of transactions per event",
                now=c.utcnow_chat_format(),
                room=room,
                selling=True,
            )
        return render_template(
            "chat/sell/ticket_quantity.html",
            event_name=event.name,
            event_unique_id=event.unique_id,
            event_category_id=event.category_id,
            room=room,
            now=c.utcnow_chat_format(),
        )
    return render_template(
        "chat/sell/event_name.html",
        event_category_id=params.event_category_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@sell_blueprint.route("/get_event_url")
@login_required
def get_event_url():
    params = c.validate_event_sell_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.create_event:
        return render_template(
            "chat/sell/event_url.html",
            event_name=params.event_name,
            event_category_id=params.event_category_id,
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.event_name:
        log(log.ERROR, "No event name provided: [%s]", params.event_name)
        return render_template(
            "chat/sell/event_name.html",
            error_message="Something went wrong, please, add event name",
            room=room,
            now=c.utcnow_chat_format(),
            event_category_id=params.event_category_id,
        )

    if not params.user_message:
        log(log.ERROR, "No event url provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_name.html",
            error_message="No event url provided. Please add event url",
            room=room,
            now=c.utcnow_chat_format(),
            event_category_id=params.event_category_id,
        )

    event = c.create_event(params, room, current_user)

    c.save_message(
        "Please provide us with a link of event👇",
        f"{params.user_message[8:25]}...",
        room,
    )

    return render_template(
        "chat/sell/event_location.html",
        event_unique_id=event.unique_id,
        event_category_id=params.event_category_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@sell_blueprint.route("/get_event_location")
@login_required
def get_event_location():
    params = c.validate_event_sell_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.user_message:
        log(log.ERROR, "No event location provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_location.html",
            error_message="No event location provided, please, add event location",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    success = c.add_event_location(params)

    if not success:
        log(log.ERROR, "Event not found, params: [%s]", params)
        return render_template(
            "chat/chat_window.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    c.save_message(
        "Got it! Please provide the city of the event.",
        f"{params.user_message}",
        room,
    )

    return render_template(
        "chat/sell/event_venue.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@sell_blueprint.route("/get_event_venue")
@login_required
def get_event_venue():
    params = c.validate_event_sell_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.user_message:
        log(log.ERROR, "No event venue provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_venue.html",
            error_message="No event venue provided, please, add event venue",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    success = c.add_event_venue(params)

    if not success:
        log(log.ERROR, "Event not found, params: [%s]", params)
        return render_template(
            "chat/chat_window.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    c.save_message(
        "Nice! Please provide the location name.",
        f"{params.user_message}",
        room,
    )

    return render_template(
        "chat/sell/event_date.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@sell_blueprint.route("/get_event_date")
@login_required
def get_event_date():
    params = c.validate_event_sell_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.user_message:
        log(log.ERROR, "No event date provided, please, add event date: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_date.html",
            error_message="No event date provided, please, add event date",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    try:
        event_date = datetime.strptime(params.user_message, app.config["CHAT_USER_FORMAT"])
    except ValueError as e:
        log(log.ERROR, "Invalid event date. Error: [%s], date: [%s]", e, params.user_message)
        return render_template(
            "chat/sell/event_date.html",
            error_message="Invalid event date, please enter a date in the format DD/MM/YYYY",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    success = c.add_event_date(params, event_date)

    if not success:
        log(log.ERROR, "Event not found, params: [%s]", params)
        return render_template(
            "chat/chat_window.html",
            error_message="Something went wrong, please, add event category",
            room=room,
            now=c.utcnow_chat_format(),
        )

    c.save_message(
        "Nice! Please specify the date",
        f"{params.user_message}",
        room,
    )

    return render_template(
        "chat/sell/event_time.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )


@sell_blueprint.route("/get_event_time")
@login_required
def get_event_time():
    params = c.validate_event_sell_params(request.args)

    room = c.get_room(params.room_unique_id)

    if not params.user_message:
        log(log.ERROR, "No event time provided: [%s]", params.user_message)
        return render_template(
            "chat/sell/event_location.html",
            error_message="No event time provided, please, add event time",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    try:
        event_time = datetime.strptime(params.user_message, "%H:%M").time()
    except ValueError as e:
        log(log.ERROR, "Invalid event time. Error: [%s], time: [%s]", e, params.user_message)
        return render_template(
            "chat/sell/event_time.html",
            error_message="Invalid event time, please enter a time in the format HH:MM",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    success = c.add_event_time(params, event_time)

    if not success:
        log(log.ERROR, "Event not found, params: [%s]", params)
        return render_template(
            "chat/chat_window.html",
            error_message="Something went wrong, please, add event details again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/sell/ticket_quantity.html",
        event_unique_id=params.event_unique_id,
        room=room,
        now=c.utcnow_chat_format(),
    )
