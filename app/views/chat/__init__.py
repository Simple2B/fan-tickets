# ruff: noqa: F401
from .main import chat_blueprint
from .auth import auth_blueprint
from .buy import buy_blueprint
from .sell import sell_blueprint
from .disputes import disputes_blueprint

chat_blueprint.register_blueprint(auth_blueprint)
chat_blueprint.register_blueprint(buy_blueprint)
chat_blueprint.register_blueprint(sell_blueprint)
chat_blueprint.register_blueprint(disputes_blueprint)
