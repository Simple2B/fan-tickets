from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired, Length


class LocationForm(FlaskForm):
    name = StringField("Location", [DataRequired(), Length(min=3, max=64)])
    picture = FileField("Picture")
    submit = SubmitField("Submit")
