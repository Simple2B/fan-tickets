from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class TicketForm(FlaskForm):
    ticket_type_choices = [
        ("general", "General"),
        ("track", "Track"),
        ("box", "Box"),
        ("back_stage", "Back Stage"),
        ("other", "Other"),
    ]

    ticket_category_choices = [
        ("student", "Student"),
        ("elderly", "Elderly"),
        ("social", "Social"),
        ("other", "Other"),
    ]

    description = StringField("Description", [DataRequired(), Length(min=3, max=256)])
    warning = StringField("Warning", [DataRequired(), Length(min=3, max=64)])
    ticket_type = SelectField("Category", choices=ticket_type_choices)
    ticket_category = SelectField("Category", choices=ticket_category_choices)
    section = StringField("Section", [DataRequired(), Length(min=3, max=16)])
    queue = StringField("Queue", [DataRequired(), Length(min=3, max=16)])
    seat = StringField("Seat", [DataRequired(), Length(min=3, max=16)])
    price_net = StringField("Price Net", [DataRequired(), Length(min=3, max=16)])
    price_gross = StringField("Price Gross")

    submit = SubmitField("Login")
