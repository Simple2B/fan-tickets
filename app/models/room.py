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

    Remark:
    - rooms'/conversations' list should be displayed on the room page

    Routes:
    - GET /rooms (admin/client)
    - GET /rooms/{room_unique_id} (admin/client)
    - GET /rooms/by_ticket/{ticket_unique_id} (admin, ajax sort)
    - GET /rooms/by_user/{user_unique_id} (admin, ajax sort)
    - POST /rooms/create (admin/client)
    - DELETE /rooms/delete/{room_unique_id}  (admin/client)
    - DELETE /rooms/delete_by_ticket/{ticket_unique_id} - do not need this

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
