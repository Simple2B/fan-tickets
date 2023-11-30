from typing import Any
from datetime import datetime
from flask import request, Blueprint, render_template
from app import models as m, db
from app import schema as s

from config import config

CFG = config()


chat_blueprint = Blueprint("chat", __name__, url_prefix="/chat")


@chat_blueprint.route("/", methods=["GET", "POST"])
def get_all():
    ...
    return render_template(
        "chat/chat_01.html",
    )
