from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class OrderCreateForm(FlaskForm):
    # TODO remove default value for document_identity_number
    document_identity_number = StringField("Document Identity Number", default="93095135270")
    card_number = StringField("Card Number", validators=[DataRequired()])
    expire = StringField("Expire", validators=[DataRequired()])
    exp_month = IntegerField("Expiration Month")
    exp_year = IntegerField("Expiration Year")
    cvv = StringField("CVV code", validators=[DataRequired()])
    room_unique_id = StringField("Chat Room ID", validators=[DataRequired()])

    def validate_expire(self, field):
        exp_values = field.data.split("/")

        if not len(exp_values) != 2:
            raise ValueError("Invalid expire date")

        exp_month, exp_year = exp_values

        try:
            exp_month = int(exp_month)
            exp_year = int(exp_year)
        except ValueError:
            ValueError("Invalid expire date")

        if exp_month < 1 or exp_month > 12:
            raise ValueError("Invalid expire date")

        if int(str(date.today().year)[2:]) >= exp_year:
            raise ValueError("Invalid expire date")

        self.exp_month.data = exp_month
        self.exp_year.data = exp_year
