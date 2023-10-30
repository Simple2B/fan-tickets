from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


if TYPE_CHECKING:
    from .ticket import Ticket
    from .message import Message


class RoomType(Enum):
    CHAT = "chat"
    DISPUTE = "dispute"


class Room(db.Model, ModelMixin):
    """
    Model for chat or dispute messages.

    Routes:
    - GET /rooms
    - GET /rooms/{room_unique_id}
    - GET /rooms/by_ticket/{ticket_unique_id}
    - GET /rooms/by_user/{user_unique_id}
    - POST /rooms/create
    - PUT /rooms/update/{room_unique_id} - to change room type from chat to dispute (to save messages' history)
    - DELETE /rooms/delete/{room_unique_id}
    - DELETE /rooms/delete_by_ticket/{ticket_unique_id}

    """

    __tablename__ = "rooms"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
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
