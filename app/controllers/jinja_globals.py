import os
import pytz
from datetime import datetime
from flask import current_app as app
from flask_wtf import FlaskForm
from flask_login import current_user
from app import models as m, db


def form_hidden_tag():
    form = FlaskForm()
    return form.hidden_tag()


def date_from_datetime(created_at: datetime):
    return created_at.date()


def time_delta(created_at: datetime) -> int:
    now = datetime.now(pytz.utc)
    if os.environ.get("APP_ENV") == "testing":
        now = datetime.now()
    return (now - created_at).days * -1


def cut_seconds(created_at: datetime = datetime.now()) -> str:
    return created_at.strftime("%Y-%m-%d %H:%M")


def card_mask(card_number: str = "000000000000000000") -> str:
    return f"{card_number[:4]} **** **** {card_number[-4:]}"


def get_categories() -> list[m.Category]:
    return m.Category.all()


def get_chat_room_messages():
    if current_user.is_authenticated:
        room_query = m.Room.select().where(m.Room.seller_id == current_user.id)
        room = db.session.scalar(room_query)
        if not room:
            return None
        return room.messages


def get_chatbot_id():
    return app.config.get("CHAT_DEFAULT_BOT_ID")


def round_to_two_places(number: float) -> float:
    return round(number, 2)
