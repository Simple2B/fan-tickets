import os
import pytz
from datetime import datetime, timedelta
import sqlalchemy as sa
from flask import current_app as app
from flask_wtf import FlaskForm
from flask_login import current_user
from app import models as m, db


def today():
    return datetime.today().strftime("%Y/%m/%d")


def form_hidden_tag():
    form = FlaskForm()
    return form.hidden_tag()


def date_from_datetime(date_time: datetime):
    return date_time.date()


def event_form_date(date_time: datetime):
    return date_time.strftime("%m/%d/%Y")


def time_delta(created_at: datetime) -> int:
    now = datetime.now(pytz.utc)
    if os.environ.get("APP_ENV") == "testing":
        now = datetime.now()
    return (now - created_at).days * -1


def cut_seconds(created_at: datetime = datetime.now()) -> str:
    return created_at.strftime("%Y-%m-%d %H:%M")


def card_mask(card_number: str = "000000000000000000") -> str:
    return f"{card_number[:4]} **** **** {card_number[-4:]}"


def get_categories() -> list[m.Category]:
    return m.Category.all()


def get_chatbot_id():
    return app.config.get("CHAT_DEFAULT_BOT_ID")


def round_to_two_places(number: float) -> float:
    return round(number, 2)


def get_ticket_subsequential_number(ticket_id: int) -> str:
    return str(ticket_id).zfill(8)


def get_paired_wallet_id(ticket_unique_id: str) -> str:
    ticket_query = m.Ticket.select().where(m.Ticket.pair_unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    wallet_id = ticket.wallet_id if ticket.wallet_id else "no wallet id found"
    return wallet_id


def get_price_gross(ticket: m.Ticket) -> int:
    user: m.User = current_user
    global_fee_settings = db.session.scalar(sa.select(m.GlobalFeeSettings))

    if user.is_authenticated and user.service_fee is not None:
        service_fee = user.service_fee
    else:
        service_fee = global_fee_settings.service_fee

    if user.is_authenticated and user.bank_fee is not None:
        bank_fee = user.bank_fee
    else:
        bank_fee = global_fee_settings.bank_fee
    total_commission = 1 + (service_fee + bank_fee) / 100

    price_net = ticket.price_net if ticket.price_net else 0
    price_gross = int(round(price_net * total_commission))

    return price_gross


def transactions_last_month(user: m.User) -> int:
    """
    The function to get last month transactions number.
    """
    tickets_query = sa.select(m.Ticket).where(
        sa.or_(m.Ticket.seller_id == user.id, m.Ticket.buyer_id == user.id),
        m.Ticket.is_sold.is_(True),
        m.Ticket.last_reservation_time > datetime.now() - timedelta(days=30),
    )
    tickets: list[m.Ticket] = db.session.scalars(tickets_query).all()

    return len(tickets)


def get_room_messages(room: m.Room) -> list[m.Message]:
    message_query = room.messages.select().order_by(m.Message.created_at)
    messages: list[m.Message] = db.session.scalars(message_query).all()

    return messages
