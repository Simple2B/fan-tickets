from datetime import datetime
import pytz
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from flask import current_app as app
from app.database import db
from .utils import ModelMixin, gen_uuid


if TYPE_CHECKING:
    from .user import User
    from .event import Event
    from .room import Room


def now():
    if app.config["TESTING"]:
        return datetime.now()
    return datetime.now(pytz.utc)


class TicketType(Enum):
    TRACK = "track"
    BOX = "box"
    BACK_STAGE = "back_stage"


class TicketCategory(Enum):
    LOT = "lot"
    SOCIAL_ENTRY = "social_entry"
    ENTIRE = "entire"


class Ticket(db.Model, ModelMixin):
    """
    Model for events

    Questions:
    - how to compare tickets

    Routes:
    - POST /tickets/create
    - POST /tickets/select_event
    - POST /tickets/type
    - POST /tickets/upload
    - POST /tickets/image_list
    - POST /tickets/add_details
    - POST /tickets/set_price
    - POST /tickets/user_details
    - POST /tickets/payment_overview_ticket_details
    - POST /tickets/payment_overview_bank_info
    - POST /tickets/phone_number
    - POST /tickets/share

    - GET /tickets_for_sale
    - GET /tickets_buy
    - GET /tickets/{ticket_unique_id}
    - GET /tickets/cart
    - GET /tickets/payment_method
    - GET /tickets/credit_card
    - GET /tickets/billing_address
    - GET /tickets/thank_you_page
    - GET /tickets/compare/{ticket_unique_id}/{ticket_unique_id}
    - GET /tickets/by_event/{event_unique_id}
    - GET /tickets/by_user/{user_unique_id}
    - GET /tickets/by_location/{location_unique_id}
    - GET /tickets/by_category/{category_unique_id}
    - PUT /tickets/update/{ticket_unique_id} - ???
    - DELETE /tickets/delete/{ticket_unique_id}
    - DELETE /tickets/delete_by_event/{event_unique_id}

    Payment system actions:
    reserve
    buy
    cancel
    refund
    transfer
    send_to_buyer
    mark_as_paid
    confirm_receive
    mark_as_sold
    mark_as_available
    mark_as_unavailable
    mark_as_in_cart
    delete_from_cart

    Change payment credentials

    """

    __tablename__ = "tickets"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )

    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )

    description: orm.Mapped[str] = orm.mapped_column(
        sa.String(512),
        unique=False,
        nullable=False,
    )

    ticket_type: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), default=TicketType.TRACK.value
    )

    ticket_category: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), default=TicketCategory.LOT.value
    )

    # The ticket file could be a PDF or a stringed QR code
    # TODO: add relation to many tickets (one to many relationship)
    file: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary, nullable=True)
    wallet_qr_code: orm.Mapped[bytes] = orm.mapped_column(sa.String(512), nullable=True)

    warning: orm.Mapped[str] = orm.mapped_column(
        sa.String(512), unique=False, nullable=True
    )

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
    )

    section: orm.Mapped[str] = orm.mapped_column(
        sa.String(16),
        nullable=False,
    )
    queue: orm.Mapped[str] = orm.mapped_column(
        sa.String(16),
        nullable=False,
    )

    seat: orm.Mapped[str] = orm.mapped_column(
        sa.String(16),
        nullable=False,
    )

    price_net: orm.Mapped[float] = orm.mapped_column(
        sa.Float,
        nullable=False,
    )
    price_gross: orm.Mapped[float] = orm.mapped_column(
        sa.Float,
        nullable=False,
    )

    quantity: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        nullable=False,
        default=1,
    )

    is_in_cart: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        default=False,
    )
    is_reserved: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        default=False,
    )
    is_sold: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        default=False,
    )
    seller_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=False
    )

    buyer_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id"),
        nullable=True,
    )
    event_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("events.id"), nullable=False
    )

    event: orm.Mapped["Event"] = orm.relationship(back_populates="tickets")

    seller: orm.Mapped["User"] = orm.relationship(
        foreign_keys=[seller_id],
        back_populates="tickets_for_sale",
    )
    buyer: orm.Mapped["User"] = orm.relationship(
        foreign_keys=[buyer_id],
        back_populates="tickets_bought",
    )

    rooms: orm.Mapped[list["Room"]] = orm.relationship(
        back_populates="ticket",
    )

    def __repr__(self):
        return f"<Ticket {self.id} of {self.event.name}>"

    @property
    def is_available(self):
        if self.event.date_time > now():
            return False
        if self.is_in_cart:
            return False
        if self.is_reserved:
            return False
        return True
