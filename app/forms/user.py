from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    BooleanField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import current_user

from app import models as m
from app import db


class UserForm(FlaskForm):
    next_url = StringField("next_url")
    user_id = StringField("user_id", [DataRequired()])
    email = StringField("email", [DataRequired(), Email()])
    activated = BooleanField("activated")
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Save")

    def validate_username(self, field):
        query = (
            m.User.select()
            .where(m.User.username == field.data)
            .where(m.User.id != int(self.user_id.data))
        )
        if db.session.scalar(query) is not None:
            raise ValidationError("This username is taken.")

    def validate_email(self, field):
        query = (
            m.User.select()
            .where(m.User.email == field.data)
            .where(m.User.id != int(self.user_id.data))
        )
        if db.session.scalar(query) is not None:
            raise ValidationError("This email is already registered.")


class NewUserForm(FlaskForm):
    email = StringField("email", [DataRequired(), Email()])
    activated = BooleanField("activated")
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Save")

    def validate_username(self, field):
        query = m.User.select().where(m.User.username == field.data)
        if db.session.scalar(query) is not None:
            raise ValidationError("This username is taken.")

    def validate_email(self, field):
        query = m.User.select().where(m.User.email == field.data)
        if db.session.scalar(query) is not None:
            raise ValidationError("This email is already registered.")


class EmailEditForm(FlaskForm):
    email = StringField("email", [DataRequired(), Email()])
    submit = SubmitField("Save")

    def validate_email(self, field):
        query = (
            m.User.select()
            .where(m.User.email == field.data)
            .where(m.User.id != current_user.id)
        )
        if db.session.scalar(query):
            raise ValidationError("This email is already registered.")


class PhoneEditForm(FlaskForm):
    phone = StringField("phone", [DataRequired()])
    submit = SubmitField("Save")

    def validate_phone(self, field):
        query = (
            m.User.select()
            .where(m.User.phone == field.data)
            .where(m.User.id != current_user.id)
        )
        if db.session.scalar(query):
            raise ValidationError("This phone is already registered.")


class CardEditForm(FlaskForm):
    card = StringField("card", [DataRequired()])
    submit = SubmitField("Save")

    def validate_card(self, field):
        query = (
            m.User.select()
            .where(m.User.card == field.data)
            .where(m.User.id != current_user.id)
        )
        if db.session.scalar(query):
            raise ValidationError("This card is already registered.")
