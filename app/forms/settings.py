from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import Optional
from app.models.global_fee_settings import TicketsSortingType


class FeeSettingsForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sorting_types = [sorting_type.value for sorting_type in TicketsSortingType]

        if "sorting_type" in kwargs:
            sorting_type = kwargs["sorting_type"]
            sorting_types.remove(sorting_type)
            self.tickets_sorting_by.choices = [(sorting_type, sorting_type)]

            self.tickets_sorting_by.choices.extend([(sorting_type, sorting_type) for sorting_type in sorting_types])

    service_fee = IntegerField("service_fee", validators=[Optional()])
    bank_fee = IntegerField("bank_fee", validators=[Optional()])

    tickets_sorting_by = SelectField("tickets_sorting_by", choices=[], validators=[Optional()])
    submit = SubmitField("Save")
