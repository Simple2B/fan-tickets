from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid, utcnow


if TYPE_CHECKING:
    from .user import User
    from .event import Event
    from .room import Room


def now():
    return datetime.now()


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
    """

    __tablename__ = "tickets"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )

    description: orm.Mapped[str | None] = orm.mapped_column(sa.String(512))

    ticket_type: orm.Mapped[str] = orm.mapped_column(sa.String(32), default=TicketType.TRACK.value)

    ticket_category: orm.Mapped[str] = orm.mapped_column(sa.String(32), default=TicketCategory.LOT.value)

    # The ticket file could be a PDF or a stringed QR code
    # TODO: add relation to many tickets (one to many relationship)
    file: orm.Mapped[bytes | None] = orm.mapped_column(sa.LargeBinary)
    wallet_qr_code: orm.Mapped[bytes | None] = orm.mapped_column(sa.String(512))

    warning: orm.Mapped[str | None] = orm.mapped_column(sa.String(512))

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=utcnow,
    )

    section: orm.Mapped[str] = orm.mapped_column(sa.String(16))
    queue: orm.Mapped[str] = orm.mapped_column(sa.String(16))

    seat: orm.Mapped[str] = orm.mapped_column(sa.String(16))

    price_net: orm.Mapped[float] = orm.mapped_column(sa.Float)
    price_gross: orm.Mapped[float] = orm.mapped_column(sa.Float)

    quantity: orm.Mapped[int] = orm.mapped_column(default=1)

    is_in_cart: orm.Mapped[bool] = orm.mapped_column(default=False)
    is_reserved: orm.Mapped[bool] = orm.mapped_column(default=False)
    is_sold: orm.Mapped[bool] = orm.mapped_column(default=False)
    seller_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))

    buyer_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("users.id"))
    event_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("events.id"))

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
