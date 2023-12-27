import sqlalchemy as sa

from flask import current_app as app

from app import controllers as c
from app import models as m, db

from app.logger import log


def get_room(room_unique_id: str) -> m.Room | None:
    room_query = sa.select(m.Room).where(m.Room.unique_id == room_unique_id)
    room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found: [%s]", room_unique_id)

    return room


def save_message(bot_message: str, user_message: str, room: m.Room):
    """
    The function to save message for history in chat.
    It is save message from chat-bot and user.
    """
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=bot_message,
    ).save(False)
    m.Message(
        room_id=room.id,
        text=user_message,
    ).save()

    log(log.INFO, "Messages for history saved. Bot: [%s], user: [%s]", bot_message, user_message)
