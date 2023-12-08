# ruff: noqa: F401
from .auth import auth_blueprint
from .main import main_blueprint
from .users import bp as user_blueprint
from .events import events_blueprint
from .tickets import tickets_blueprint
from .admin import admin_blueprint
from .chat_registration import chat_registration_blueprint
