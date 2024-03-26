import os
import re
import pytz
from datetime import datetime, timedelta
import sqlalchemy as sa
from flask import current_app as app
from flask_wtf import FlaskForm
from flask_login import current_user
from app import models as m, db
from .chat_bard_translation import bot_message_translation
from .utils import get_tickets_fees


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
    buyer: m.User = current_user
    seller: m.User = ticket.seller
    global_fee_settings = db.session.scalar(sa.select(m.GlobalFeeSettings))

    service_fee, bank_fee = get_tickets_fees(buyer, seller, global_fee_settings)
    total_commission = 1 + (service_fee + bank_fee) / 100

    price_net = ticket.price_net if ticket.price_net else 0
    price_gross = int(round(price_net * total_commission))

    return price_gross


def transactions_last_month(user: m.User) -> int:
    """
    The function to get last month transactions number.
    """
    tickets_bought_query = sa.select(m.Ticket).where(
        m.Ticket.is_deleted.is_(False),
        m.Ticket.buyer_id == user.id,
        m.Ticket.last_reservation_time > datetime.now() - timedelta(days=30),
        m.Ticket.event.has(m.Event.approved.is_(True)),
        m.Ticket.is_sold.is_(True),
    )
    tickets_bought: list[m.Ticket] = db.session.scalars(tickets_bought_query).all()

    tickets_posted_query = sa.select(m.Ticket).where(
        m.Ticket.is_deleted.is_(False),
        m.Ticket.seller_id == user.id,
        m.Ticket.created_at > datetime.now() - timedelta(days=30),
        m.Ticket.event.has(m.Event.approved.is_(True)),
    )
    tickets_posted: list[m.Ticket] = db.session.scalars(tickets_posted_query).all()

    return len(tickets_bought) + len(tickets_posted)


def transactions_per_event(user: m.User, event: m.Event) -> int:
    """
    The function to get transactions per event.
    """
    tickets_query = sa.select(m.Ticket).where(
        sa.or_(m.Ticket.seller_id == user.id, m.Ticket.buyer_id == user.id),
        m.Ticket.is_deleted.is_(False),
        m.Ticket.event_id == event.id,
        m.Ticket.event.has(m.Event.approved.is_(True)),
        m.Ticket.is_sold.is_(True),
    )
    tickets: list[m.Ticket] = db.session.scalars(tickets_query).all()

    return len(tickets)


def get_room_messages(room: m.Room) -> list[m.Message]:
    message_query = room.messages.select().order_by(m.Message.created_at)
    messages: list[m.Message] = db.session.scalars(message_query).all()

    return messages


def pt(text_en: str, chat_screen: str) -> str:
    text_en = re.sub(r"\s+", " ", text_en)

    translation_query = sa.select(m.Translation).where(m.Translation.en == text_en)
    translation: m.Translation = db.session.scalar(translation_query)

    if not translation:
        text_pt = bot_message_translation(text_en)
        translation = m.Translation(
            name=chat_screen,
            en=text_en,
            pt=text_pt,
        ).save()
        return text_en

    if translation.pt:
        translated_text = translation.pt
    else:
        translated_text = bot_message_translation(text_en)
    return translated_text
