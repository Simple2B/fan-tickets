from typing import TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User
    from .event import Event
    from .ticket import Ticket


class Payment(db.Model, ModelMixin):
    __tablename__ = "payments"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        nullable=False,
    )
    buyer_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id"),
        nullable=False,
    )
    event_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("events.id"),
        nullable=False,
    )
    ticket_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("tickets.id"),
        nullable=False,
    )
    description: orm.Mapped[str] = orm.mapped_column(
        sa.String(255),
        unique=False,
        nullable=True,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )

    event: orm.Mapped["Event"] = orm.relationship()
    ticket: orm.Mapped["Ticket"] = orm.relationship()
    buyer: orm.Mapped["User"] = orm.relationship()

    def __repr__(self):
        return f"<{self.id}:<{self.event.name}>|<{self.buyer.username}"
