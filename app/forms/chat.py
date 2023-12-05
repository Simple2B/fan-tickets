from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired
from flask_login import current_user

from app import models as m
from app import db


class ChatPhoneForm(FlaskForm):
    phone = StringField("phone", [DataRequired()])
    submit = SubmitField("Save")

    def validate_phone(self, field):
        query = m.User.select().where(m.User.phone == field.data).where(m.User.id != current_user.id)
        if db.session.scalar(query):
            raise ValidationError("This phone is already registered.")
