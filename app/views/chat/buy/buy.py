import os

from psycopg2 import IntegrityError

from flask import request, Blueprint, render_template, current_app as app, url_for
from flask_login import current_user

from app import controllers as c, schema as s, models as m, db
from app.logger import log
from app import mail_controller

from config import config


CFG = config()
DEVELOPMENT_BASE_URL = os.environ.get("SERVER_NAME")
LOCAL_WEBHOOK_URL = f"http://{DEVELOPMENT_BASE_URL}/pay/webhook"

buy_blueprint = Blueprint("buy", __name__, url_prefix="/buy")


@buy_blueprint.route("/get_event_name", methods=["GET", "POST"])
def get_event_name():
    params = c.validate_event_buy_params(request.args)

    room = c.get_room(params.room_unique_id)

    if params.renew_search:
        c.save_message("Choose action", "Renew search", room)
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

    c.save_message(
        "Great! To get started, could you please write below name of the event you're looking for?",
        f"{params.user_message}",
        room,
    )

    events = c.get_event_by_name_bard(params, room, from_buy=True)

    if not events:
        log(log.INFO, "Events not found: [%s]", params.user_message)
        return render_template(
            "chat/buy/event_not_found.html",
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
                event_unique_id=first_event.unique_id,
            )

        global_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
        tickets_cheapest = c.get_sorted_tickets(
            tickets,
            params.tickets_show_all,
            global_settings.tickets_sorting_by,
        )

        log(log.INFO, "Tickets found: [%s]", tickets)
        return render_template(
            "chat/buy/ticket_list.html",
            event_unique_id=first_event.unique_id,
            room=room,
            now=c.utcnow_chat_format(),
            tickets=tickets_cheapest,
            tickets_all_length=len(tickets),
            tickets_per_chat=app.config["TICKETS_PER_CHAT"],
            tickets_show_all=params.tickets_show_all,
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
        events=events,
        room=room,
        now=c.utcnow_chat_format(),
    )


@buy_blueprint.route("/get_events_by_location")
def get_events_by_location():
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

    if not params.location_unique_id:
        log(log.ERROR, "No location unique id provided: [%s]", params.location_unique_id)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.event_name:
        log(log.ERROR, "No event name provided: [%s]", params.event_name)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong. Please add event name",
            room=room,
            now=c.utcnow_chat_format(),
        )

    events = c.get_events_by_location_event_name(params, room)

    if not events:
        log(log.INFO, "Events not found: [%s]", params.user_message)
        return render_template(
            "chat/buy/ticket_not_found.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    first_event: m.Event = events[0]
    if len(events) == 1:
        log(log.INFO, "Only 1 event found: [%s]", params.event_name)

        tickets = c.get_tickets_by_event(first_event, room)
        if not tickets:
            log(log.ERROR, "Tickets not found: [%s]", params.user_message)
            return render_template(
                "chat/buy/ticket_not_found.html",
                room=room,
                now=c.utcnow_chat_format(),
                event_unique_id=first_event.unique_id,
            )

        global_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
        tickets_cheapest = c.get_sorted_tickets(
            tickets,
            params.tickets_show_all,
            global_settings.tickets_sorting_by,
        )

        log(log.INFO, "Tickets found: [%s]", tickets)
        return render_template(
            "chat/buy/ticket_list.html",
            event_unique_id=first_event.unique_id,
            room=room,
            now=c.utcnow_chat_format(),
            tickets=tickets_cheapest,
            tickets_all_length=len(tickets),
            tickets_per_chat=app.config["TICKETS_PER_CHAT"],
            tickets_show_all=params.tickets_show_all,
        )

    return render_template(
        "chat/buy/ticket_date.html",
        events=events,
        room=room,
        now=c.utcnow_chat_format(),
    )


@buy_blueprint.route("/subscribe_on_event")
def subscribe_on_event():
    params = c.validate_buy_ticket_params(request.args)

    room = c.get_room(params.room_unique_id)
    user: m.User = current_user

    if not params.event_unique_id:
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong, please choose event again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not current_user.is_authenticated and not params.has_email:
        log(log.INFO, "User unauthorized without email: [%s]", params.has_email)
        return render_template(
            "chat/buy/email_for_subscribe.html",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    if not current_user.is_authenticated and params.has_email and not params.user_message:
        log(log.INFO, "User unauthorized. Email is not provided: [%s]", params.user_message)
        return render_template(
            "chat/buy/email_for_subscribe.html",
            error_message="Please provide your email",
            room=room,
            now=c.utcnow_chat_format(),
            event_unique_id=params.event_unique_id,
        )

    if not current_user.is_authenticated:
        if not params.user_message:
            log(log.INFO, "User unauthorized. Email is not provided: [%s]", params.user_message)
            return render_template(
                "chat/buy/email_for_subscribe.html",
                error_message="Please provide your email",
                room=room,
                now=c.utcnow_chat_format(),
                event_unique_id=params.event_unique_id,
            )
        user = c.create_user(params.user_message)

        try:
            db.session.commit()
            log(log.INFO, "User created: [%s]", user)
        except IntegrityError as e:
            db.session.rollback()
            log(log.ERROR, "User is not created: [%s]", e)
            return render_template(
                "chat/buy/event_name.html",
                error_message="Something went wrong, please choose event again",
                room=room,
                now=c.utcnow_chat_format(),
            )

    event = c.subscribe_event(params.event_unique_id, user)

    if not event:
        log(log.ERROR, "Subscribe not found: [%s]", event)
        return render_template(
            "chat/buy/event_name.html",
            error_message="Something went wrong, please choose event again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if os.environ.get("APP_ENV") == "development":
        url = url_for(
            "auth.activate",
            reset_password_uuid=user.uuid,
            _external=True,
        )
    else:
        if os.environ.get("SERVER_TYPE") == "production":
            base_url = app.config["PRODUCTION_BASE_URL"]
        else:
            base_url = app.config["STAGING_BASE_URL"]
        url = f"{base_url}activated/{user.uuid}"

    mail_controller.send_email(
        (user,),
        f"Subscription to {CFG.APP_NAME}",
        render_template(
            "email/email_confirm_subscribe.htm",
            user=user,
            event_name=event.name,
            url=url,
        ),
    )

    c.save_message(
        "Oops, it seems like we don´t have tickets for this event😢 Would you like to be notified if a ticket appears?",
        "Yes",
        room,
    )

    return render_template(
        "chat/buy/subscribe_success.html",
        room=room,
        now=c.utcnow_chat_format(),
        email=current_user.email if current_user.is_authenticated else user.email,
    )
