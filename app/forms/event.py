from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import IntegerField, StringField, SelectField, SubmitField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, URL


class EventForm(FlaskForm):
    name = StringField("Event name", [DataRequired(), Length(min=3, max=64)])
    url = StringField("URL", [DataRequired(), URL()])
    observations = StringField("Observations", [DataRequired(), Length(min=3, max=256)])
    warning = StringField("Warning", [DataRequired(), Length(min=3, max=64)])
    date_time = DateField("Datetime", [DataRequired()], "%m/%d/%Y")
    hours = IntegerField("Hours", [DataRequired()])
    minutes = IntegerField("Hours", [DataRequired()])
    category = SelectField("Category", choices=[])
    location = SelectField("Location", choices=[])
    picture = FileField("Picture")
    approved = SelectField(
        "Approved",
        coerce=lambda s: s == "y",
        choices=[
            (
                "n",
                "Not approved",
            ),
            (
                "y",
                "Approved",
            ),
        ],
    )
    submit = SubmitField("Create event")

    def validate_hours(self, field):
        if int(field.data) > 23 or int(field.data) < 0:
            raise ValidationError("Invalid hours.")

    def validate_minutes(self, field):
        if int(field.data) > 59 or int(field.data) < 0:
            raise ValidationError("Invalid minutes.")


class EventUpdateForm(EventForm):
    submit = SubmitField("Save event")
