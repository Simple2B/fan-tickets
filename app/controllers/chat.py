import sqlalchemy as sa
from flask import current_app as app, render_template
from app.database import db
from app import models as m, schema as s, controllers as c
from app.logger import log


def get_home(user_message: str, room: m.Room) -> str:
    """
    The function to get chat home page.
    """
    log(log.INFO, "Chat home page")
    return render_template(
        "chat/chat_home.html",
        now=c.utcnow_chat_format(),
        room=room,
    )


def get_room(room_unique_id: str) -> m.Room:
    room_query = sa.select(m.Room).where(m.Room.unique_id == room_unique_id)
    room = db.session.scalar(room_query)

    if not room:
        raise ValueError(f"Room not found: {room_unique_id}")

    return room


def validate_event_sell_params(request_args) -> s.ChatSellEventParams:
    """
    The function to validate chat input params.
    """
    try:
        params = s.ChatSellEventParams.model_validate(dict(request_args))
    except Exception as e:
        raise ValueError(f"Invalid event params: {e}")

    return params


def validate_event_buy_params(request_args) -> s.ChatBuyEventParams:
    """
    The function to validate chat input params.
    """
    try:
        params = s.ChatBuyEventParams.model_validate(dict(request_args))
    except Exception as e:
        raise ValueError(f"Invalid event params: {e}")

    return params


def validate_cell_ticket_params(request_args) -> s.ChatSellTicketParams:
    """
    The function to validate chat input params.
    """
    try:
        params = s.ChatSellTicketParams.model_validate(dict(request_args))
    except Exception as e:
        raise ValueError(f"Invalid ticket params: {e}")

    return params


def validate_buy_ticket_params(request_args) -> s.ChatBuyTicketParams:
    """
    The function to validate chat input params.
    """
    try:
        params = s.ChatBuyTicketParams.model_validate(dict(request_args))
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


def ticket_details(ticket: m.Ticket, room: m.Room, buy=False) -> bool:
    date_time = ticket.event.date_time.strftime("%Y-%m-%d %H:%M") if ticket.event.date_time else ""
    ticket_details = (
        f"Event: {ticket.event.name}\n"
        + f"Location: {ticket.event.location.name}\n"
        + f"Venue: {ticket.event.venue}\n"
        + f"Date time: {date_time}\n"
        + f"Ticket type: {ticket.ticket_type}\n"
        + f"Ticket category: {ticket.ticket_category}\n"
        + f"Ticket section: {ticket.section}\n"
        + f"Ticket price net: {ticket.price_net}\n"
        + f"Ticket price gross: {ticket.price_gross}\n"
        + f"Ticket description: {ticket.description}"
    )
    if buy:
        c.save_message("We have found tickets. What ticket do you want?", "Ticket details:", room)
        m.Message(
            room_id=room.id,
            text=f"Event: {ticket.event.name}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Location: {ticket.event.location.name}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Venue: {ticket.event.venue}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Date time: {date_time}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Ticket type: {ticket.ticket_type}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Ticket category: {ticket.ticket_category}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Ticket section: {ticket.section}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Ticket price net: {ticket.price_net}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Ticket price gross: {ticket.price_gross}\n",
        ).save(False)
        m.Message(
            room_id=room.id,
            text=f"Ticket description: {ticket.description}",
        ).save()
    else:
        c.save_message(ticket_details, "Got it", room)

    return True
