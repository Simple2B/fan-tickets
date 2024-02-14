import base64
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


class TicketType(Enum):
    GENERAL = "general"
    TRACK = "track"
    BOX = "box"
    BACK_STAGE = "back_stage"
    OTHER = "other"


class TicketCategory(Enum):
    REGULAR = "regular"
    STUDENT = "student"
    ELDERLY = "elderly"
    SOCIAL = "social"
    OTHER = "other"


class Ticket(db.Model, ModelMixin):
    __tablename__ = "tickets"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    event_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("events.id"))
    seller_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))
    buyer_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("users.id"))

    # Columns
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )

    description: orm.Mapped[str | None] = orm.mapped_column(sa.String(512))

    ticket_type: orm.Mapped[str] = orm.mapped_column(sa.String(32), default=TicketType.GENERAL.value)

    ticket_category: orm.Mapped[str] = orm.mapped_column(sa.String(32), default=TicketCategory.ELDERLY.value)

    # Pair ticket
    is_paired: orm.Mapped[bool] = orm.mapped_column(default=False)
    pair_unique_id: orm.Mapped[str | None] = orm.mapped_column(sa.String(64))
    separate_selling_allowed: orm.Mapped[bool] = orm.mapped_column(default=False)

    # The ticket file could be a PDF or a stringed wallet id
    file: orm.Mapped[bytes | None] = orm.mapped_column(sa.LargeBinary)
    wallet_id: orm.Mapped[str | None] = orm.mapped_column(sa.String(512))

    warning: orm.Mapped[str | None] = orm.mapped_column(sa.String(512))

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=utcnow,
    )

    section: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))
    queue: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))

    seat: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))

    price_net: orm.Mapped[int | None] = orm.mapped_column(sa.Integer)
    price_gross: orm.Mapped[int | None] = orm.mapped_column(sa.Integer)

    quantity: orm.Mapped[int] = orm.mapped_column(default=1)

    is_in_cart: orm.Mapped[bool] = orm.mapped_column(default=False)
    is_reserved: orm.Mapped[bool] = orm.mapped_column(default=False)
    last_reservation_time: orm.Mapped[datetime | None] = orm.mapped_column(sa.DateTime)
    is_sold: orm.Mapped[bool] = orm.mapped_column(default=False)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False, server_default=sa.false())
    paid_to_seller_at: orm.Mapped[datetime | None] = orm.mapped_column(sa.DateTime, server_default=sa.text("NULL"))

    # Relationships
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
        if self.event.date_time < utcnow():
            return False
        if self.is_deleted:
            return False
        if self.is_sold:
            return False
        if self.is_reserved:
            return False
        return True

    @property
    def base64_src(self) -> str:
        """
        Returns the base64 representation of the picture.
        """
        if self.file:
            base64_img = base64.b64encode(self.file).decode("utf-8")
            return f"data:application/pdf;base64,{ base64_img }"
        return ""
