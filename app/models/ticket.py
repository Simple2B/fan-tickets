from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User
    from .event import Event
    from .room import Room


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

    Actions in admin section:
    - create
    - read
    - delete

    - quantity, original value, sales value
    - observations/conditions
    - read ticket barcode / QRcode
    - insert warning
    - net amount (price)
    - the amount the buyer should pay
    """

    __tablename__ = "tickets"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
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
    file: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary, nullable=True)
    wallet_qr_code: orm.Mapped[bytes] = orm.mapped_column(sa.String(512), nullable=True)

    warning: orm.Mapped[str] = orm.mapped_column(
        sa.String(512), unique=False, nullable=True
    )

    seller_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey(User.id), nullable=False
    )

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
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

    buyer_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey(User.id),
        nullable=True,
    )
    event_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey(Event.id), nullable=False
    )

    event: orm.Mapped["Event"] = orm.relationship(back_populates="tickets")

    seller: orm.Mapped["User"] = orm.relationship(
        "User",
        back_populates="tickets_for_sale",
    )
    buyer: orm.Mapped["User"] = orm.relationship(
        "User",
        back_populates="tickets_bought",
    )

    rooms: orm.Mapped[list["Room"]] = orm.relationship(
        "Room",
        back_populates="ticket",
    )

    @property
    def is_available(self):
        if self.created_at > datetime.utcnow():
            return False
        if self.is_in_cart:
            return False
        if self.is_reserved:
            return False
        return True
