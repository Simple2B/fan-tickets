from datetime import datetime
from random import randint
import re

from flask import render_template, current_app as app
from flask_mail import Message

from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db, mail

from app.logger import log
from config import config

CFG = config()


def check_room_id(params: s.ChatSellParams) -> tuple[s.ChatSellResultParams, m.Room | None]:
    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == params.room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    # TODO: is needed to create a room if it does not exist?
    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return s.ChatSellResultParams(now_str=now_str, is_error=True), room

    if not params.room_unique_id:
        log(
            log.ERROR,
            "Form submitting error, room_unique_id: [%s]",
            params.room_unique_id,
        )
        return s.ChatSellResultParams(now_str=now_str, is_error=True), room

    return s.ChatSellResultParams(now_str=now_str), room


def send_message(bot_message: str, user_message: str, room: m.Room):
    """
    The function to save message for history in chat.
    It is save message from chat-bot and user.
    """
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=bot_message,
    ).save(False)
    m.Message(
        room_id=room.id,
        text=user_message,
    ).save()

    log(log.INFO, "Messages for history saved. Bot: [%s], user: [%s]", bot_message, user_message)


def create_event(params: s.ChatSellParams, room: m.Room):
    location_query = m.Location.select().where(m.Location.name == params.event_location)
    location = db.session.scalar(location_query)

    if not location:
        location = m.Location(name=params.event_location).save()

    event_date = datetime.strptime(f"{params.event_date} {params.event_time}", app.config["DATE_CHAT_HISTORY_FORMAT"])
    event_query = m.Event.select().where(
        m.Event.name == params.event_name,
        m.Event.location == location,
        m.Event.date_time == event_date,
    )
    event = db.session.scalar(event_query)

    if not event:
        event = m.Event(
            name=params.event_name,
            location=location,
            date_time=event_date,
        ).save()
