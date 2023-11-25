import os
import pytz
from datetime import datetime
from flask_wtf import FlaskForm


def form_hidden_tag():
    form = FlaskForm()
    return form.hidden_tag()


def date_from_datetime(created_at: datetime):
    return created_at.date()


def time_delta(created_at: datetime):
    now = datetime.now(pytz.utc)
    if os.environ.get("APP_ENV") == "testing":
        now = datetime.now()
    return (now - created_at).days * -1


def cut_seconds(created_at: datetime):
    return created_at.strftime("%Y-%m-%d %H:%M")


def card_mask(card_number: str):
    return f"{card_number[:4]} **** **** {card_number[-4:]}"
