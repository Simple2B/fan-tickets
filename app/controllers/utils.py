from datetime import datetime, UTC

from flask import current_app as app


def utcnow_chat_format():
    now = datetime.now(UTC)
    return now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])
