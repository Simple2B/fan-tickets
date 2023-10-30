from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .ticket import Ticket
    from .message import Message


class RoomType(Enum):
    CHAT = "chat"
    DISPUTE = "dispute"


class Room(db.Model, ModelMixin):
    """
    Model for chat or dispute messages
    """

    __tablename__ = "rooms"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )

    type_of: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), default=RoomType.CHAT.value
    )

    is_open: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
    )

    ticket_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("tickets.id"),
        nullable=False,
    )

    ticket: orm.Mapped["Ticket"] = orm.relationship(
        "Ticket",
        back_populates="rooms",
    )
    messages: orm.Mapped[list["Message"]] = orm.relationship(
        "Message",
        back_populates="room",
    )
