from datetime import datetime, timedelta
from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_required
from app import models as m, db
from app.logger import log
from config import config

CFG = config()

chat_buy_blueprint = Blueprint("buy", __name__, url_prefix="/buy")


@chat_buy_blueprint.route("/", methods=["GET", "POST"])
@login_required
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
        log(log.ERROR, "No event name provided: [%s]", location_input)
        error_message += "No event name provided \n"

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
        "chat/buy/events_02_list.html",
        now=now_str,
        room=room,
        events=events,
        event_location=location_input,
        event_date=date_input,
    )
