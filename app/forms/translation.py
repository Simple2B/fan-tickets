from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class TranslationForm(FlaskForm):
    name = StringField("Name")
    en = TextAreaField("English", validators=[DataRequired()])
    pt = TextAreaField("Portuguese")
    submit = SubmitField("Submit")
