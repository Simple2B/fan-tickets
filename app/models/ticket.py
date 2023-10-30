from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid
from .users_tickets import users_tickets


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

    Routes:
    - POST /tickets/create (client)
    - GET /tickets (client)
    - GET /tickets/{ticket_unique_id} (client)
    - GET /tickets/by_event/{event_unique_id} (client, ajax sort query params)
    - GET /tickets/by_user/{user_unique_id} (client, ajax sort query params)
    - GET /tickets/by_location/{location_unique_id} (client, ajax sort query params)
    - GET /tickets/by_category/{category_unique_id} (client, ajax sort query params)
    - PUT /tickets/update/{ticket_unique_id} - do not need this
    - DELETE /tickets/delete/{ticket_unique_id} (admin)
    - DELETE /tickets/delete_by_event/{event_unique_id} (admin)
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
        "User",
        secondary=users_tickets,
        back_populates="tickets_for_sale",
    )
    buyer: orm.Mapped["User"] = orm.relationship(
        "User",
        secondary=users_tickets,
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
