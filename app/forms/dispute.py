from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    room_unique_id = StringField("room_unique_id", [DataRequired()])
    message = StringField("message", [DataRequired()])
