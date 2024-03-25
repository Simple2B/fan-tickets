# ruff: noqa: F401
from .buy import buy_blueprint
from .ticket import ticket_blueprint
from .payment import payment_blueprint

buy_blueprint.register_blueprint(ticket_blueprint)
buy_blueprint.register_blueprint(payment_blueprint)
