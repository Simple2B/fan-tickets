from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, URL


class EventForm(FlaskForm):
    name = StringField("Event name", [DataRequired(), Length(min=3, max=64)])
    url = StringField("URL", [DataRequired(), URL()])
    observations = StringField("Observations", [DataRequired(), Length(min=3, max=256)])
    warning = StringField("Warning", [DataRequired(), Length(min=3, max=64)])
    date_time = DateField("Datetime", [DataRequired()], "%m/%d/%Y")
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


class EventUpdateForm(EventForm):
    submit = SubmitField("Save event")
