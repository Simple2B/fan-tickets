import pytz
from datetime import datetime
from flask_wtf import FlaskForm


def form_hidden_tag():
    form = FlaskForm()
    return form.hidden_tag()


def date_from_datetime(created_at: datetime):
    return created_at.date()


def time_delta(created_at: datetime):
    return (datetime.now(pytz.utc) - created_at).days * -1


def cut_seconds(created_at: datetime):
    return created_at.strftime("%Y-%m-%d %H:%M")
