import os
import pytz
from datetime import datetime

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


def get_chat_room_messages():
    if not current_user.is_authenticated:
        return None

    room = db.session.scalar(sa.select(m.Room).where(m.Room.seller_id == current_user.id))
    if not room:
        return None

    return db.session.scalars(room.messages.select())


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
