import re
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    ValidationError,
    FileField,
)
from wtforms.validators import DataRequired
from flask_login import current_user

from app import models as m
from app.database import db


class ChatFileUploadForm(FlaskForm):
    room_unique_id = StringField("room_unique_id", [DataRequired()])
    user_unique_id = StringField("user_unique_id", [DataRequired()])
    file = FileField("file", [DataRequired()])
    submit = SubmitField("Send verification code")


class ChatPhoneForm(FlaskForm):
    phone = StringField("phone", [DataRequired()])
    submit = SubmitField("Save")

    def validate_phone(self, field):
        pattern = r"^\+?\d{10,13}$"
        match_pattern = re.search(pattern, field.data)
        if not match_pattern:
            raise ValidationError("Invalid phone number.")

        query = m.User.select().where(m.User.phone == field.data).where(m.User.id != current_user.id)
        if db.session.scalar(query):
            raise ValidationError("This phone is already registered.")


class ChatAuthPasswordForm(FlaskForm):
    room_unique_id = StringField("room_unique_id", [DataRequired()])
    user_unique_id = StringField("user_unique_id", [DataRequired()])
    password = StringField("password", [DataRequired()])
    submit = SubmitField("Send verification code")
