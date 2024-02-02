import sqlalchemy as sa
from flask import current_app as app
from app.database import db
from app import models as m, schema as s
from app.logger import log


def get_room(room_unique_id: str) -> m.Room:
    room_query = sa.select(m.Room).where(m.Room.unique_id == room_unique_id)
    room = db.session.scalar(room_query)

    if not room:
        raise ValueError(f"Room not found: {room_unique_id}")

    return room


def validate_event_params(request_args) -> s.ChatSellEventParams:
    """
    The function to validate chat input params.
    """
    try:
        params = s.ChatSellEventParams.model_validate(dict(request_args))
    except Exception as e:
        raise ValueError(f"Invalid event params: {e}")

    return params


def validate_ticket_params(request_args) -> s.ChatSellTicketParams:
    """
    The function to validate chat input params.
    """
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request_args))
    except Exception as e:
        raise ValueError(f"Invalid ticket params: {e}")

    return params


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
