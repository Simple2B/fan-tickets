from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LocationForm(FlaskForm):
    name = StringField("Username", [DataRequired(), Length(min=3, max=64)])
    submit = SubmitField("Login")
