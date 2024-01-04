from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
import sqlalchemy as sa
from app import models as m
from app import db


class EventForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = db.session.scalars(sa.select(m.Category)).all()
        locations = db.session.scalars(sa.select(m.Location)).all()

        if "category" in kwargs.keys():
            category = kwargs["category"]
            categories.remove(category)
            self.category.choices.append((category.id, category.name))

        for category in categories:
            self.category.choices.append((category.id, category.name))

        if "location" in kwargs.keys():
            location = kwargs["location"]
            locations.remove(location)
            self.location.choices.append((location.id, location.name))

        for location in locations:
            self.location.choices.append((location.id, location.name))

    name = StringField("Username", [DataRequired(), Length(min=3, max=64)])
    url = StringField("URL", [DataRequired(), Length(min=3, max=256)])
    observations = StringField("Observations", [DataRequired(), Length(min=3, max=64)])
    warning = StringField("Warning", [DataRequired(), Length(min=3, max=64)])
    date_time = StringField("DateTime", [DataRequired()])
    category = SelectField("Category", choices=[])
    location = SelectField("Location", choices=[])
    submit = SubmitField("Login")
