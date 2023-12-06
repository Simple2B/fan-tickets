from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app.models import User
from app import db


class LoginForm(FlaskForm):
    user_id = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 30)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    # phone = StringField("Phone", validators=[DataRequired(), Length(7, 16)])
    # card = StringField("Card", validators=[DataRequired(), Length(16, 16)])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(form, field):
        query = User.select().where(User.username == field.data)
        if db.session.scalar(query) is not None:
            raise ValidationError("This username is taken.")

    def validate_email(form, field):
        query = User.select().where(User.email == field.data)
        if db.session.scalar(query) is not None:
            raise ValidationError("This email is already registered.")


class PhoneRegistrationForm(FlaskForm):
    phone = StringField("Phone", validators=[DataRequired(), Length(7, 16)])
    submit = SubmitField("Register")

    def validate_phone(form, field):
        query = User.select().where(User.phone == field.data)
        if db.session.scalar(query) is not None:
            raise ValidationError("This phone number is taken.")


class VerificationCodeForm(FlaskForm):
    digit_1 = StringField("Digit", validators=[DataRequired(), Length(1, 1)])
    digit_2 = StringField("Digit", validators=[DataRequired(), Length(1, 1)])
    digit_3 = StringField("Digit", validators=[DataRequired(), Length(1, 1)])
    digit_4 = StringField("Digit", validators=[DataRequired(), Length(1, 1)])
    digit_5 = StringField("Digit", validators=[DataRequired(), Length(1, 1)])
    digit_6 = StringField("Digit", validators=[DataRequired(), Length(1, 1)])


class ForgotForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])

    def validate_email(self, email):
        query = User.select().where(User.email == email.data)
        user = db.session.scalar(query)
        if not user:
            raise ValidationError("Email not found")


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        [
            DataRequired(),
            EqualTo("password_confirmation", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Password"},
    )
    password_confirmation = PasswordField("Repeat Password", render_kw={"placeholder": "Repeat Password"})
    submit = SubmitField("Change password")
