from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import Optional


class FeeSettingsForm(FlaskForm):
    service_fee = IntegerField("service_fee", validators=[Optional()])
    bank_fee = IntegerField("bank_fee", validators=[Optional()])
    submit = SubmitField("Save")
