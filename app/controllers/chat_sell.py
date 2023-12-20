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


def check_room_id(params: s.ChatAuthParams) -> tuple[s.ChatAuthResultParams, m.User | None, m.Room | None]:
    """
    The function to check and validate params.
    At the moment it returns response with template for chat if params are not valid or
    return params, room, user, datetime as string if params are valid.
    """
    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == params.room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    # TODO: is needed to create a room if it does not exist?
    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return s.ChatAuthResultParams(now_str=now_str, params=params, is_error=True), None, room

    if not params.room_unique_id or not params.user_unique_id:
        log(
            log.ERROR,
            "Form submitting error, user_unique_id: [%s], room_unique_id: [%s]",
            params.user_unique_id,
            params.room_unique_id,
        )
        return s.ChatAuthResultParams(now_str=now_str, params=params, is_error=True), None, room

    user_query = m.User.select().where(m.User.unique_id == params.user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return s.ChatAuthResultParams(now_str=now_str, params=params, is_error=True), user, room

    return s.ChatAuthResultParams(now_str=now_str, params=params, user=user), user, room
