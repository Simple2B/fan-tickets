from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField


class IndividualSettingsForm(FlaskForm):
    service_fee = IntegerField("service_fee")
    bank_fee = IntegerField("bank_fee")
    submit = SubmitField("Save")
