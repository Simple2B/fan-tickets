from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class TicketForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ticket_types = [
            ("general", "General"),
            ("track", "Track"),
            ("box", "Box"),
            ("back_stage", "Back Stage"),
            ("other", "Other"),
        ]

        if "ticket_type" in kwargs.keys():
            ticket_type = kwargs["ticket_type"]
            for item in ticket_types:
                if item[0] == ticket_type:
                    ticket_types.remove(item)
                    self.ticket_type.choices.append(item)

        for item in ticket_types:
            self.ticket_type.choices.append(item)

        ticket_category_choices = [
            ("student", "Student"),
            ("elderly", "Elderly"),
            ("social", "Social"),
            ("other", "Other"),
        ]

        if "ticket_category" in kwargs.keys():
            ticket_category = kwargs["ticket_category"]
            for item in ticket_category_choices:
                if item[0] == ticket_category:
                    ticket_category_choices.remove(item)
                    self.ticket_category.choices.append(item)

        for item in ticket_category_choices:
            self.ticket_category.choices.append(item)

        deleted_choices = [("True", "Deleted"), ("False", "Active")]

        if "ticket_deleted" in kwargs.keys():
            deleted = kwargs["ticket_deleted"]
            for item in deleted_choices:
                if item[0] == str(deleted):
                    deleted_choices.remove(item)
                    self.deleted.choices.append(item)

        for item in deleted_choices:
            self.deleted.choices.append(item)

    description = StringField("Description", [DataRequired(), Length(min=0, max=256)])
    warning = StringField("Warning", [DataRequired(), Length(min=0, max=256)])
    ticket_type = SelectField("Category", choices=[])
    ticket_category = SelectField("Category", choices=[])
    deleted = SelectField("Deleted", choices=[])
    section = StringField("Section", [DataRequired(), Length(min=3, max=16)])
    queue = StringField("Queue", [DataRequired(), Length(min=3, max=16)])
    seat = StringField("Seat", [DataRequired(), Length(min=3, max=16)])
    price_net = StringField("Price Net", [DataRequired(), Length(min=3, max=16)])
    price_gross = StringField("Price Gross")

    submit = SubmitField("Login")
