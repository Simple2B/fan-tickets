import os
import base64
import pytz
from datetime import datetime
from flask_wtf import FlaskForm
from app import models as m, db


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


def stream_picture(picture_id):
    picture_query = m.Picture.select().where(m.Picture.id == picture_id)
    picture = db.session.scalar(picture_query)
    img_byte_arr = picture.file
    base64_img = base64.b64encode(img_byte_arr).decode("utf-8")
    return base64_img
