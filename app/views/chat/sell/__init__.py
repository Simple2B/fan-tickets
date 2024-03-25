# ruff: noqa: F401
from .sell import sell_blueprint
from .ticket import ticket_blueprint
from .ticket_details import ticket_details_blueprint

sell_blueprint.register_blueprint(ticket_blueprint)
sell_blueprint.register_blueprint(ticket_details_blueprint)
