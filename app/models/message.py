from datetime import datetime
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User
    from .room import Room


class Message(db.Model, ModelMixin):
    """
    Model for chat or dispute messages
    """

    __tablename__ = "messages"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    sender_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id"),
        nullable=False,
    )
    room_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("rooms.id"),
        nullable=False,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
    )
    viewed: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        default=False,
    )
    text: orm.Mapped[str] = orm.mapped_column(
        sa.String(512),
        nullable=False,
    )

    sender: orm.Mapped["User"] = orm.relationship()
    room: orm.Mapped["Room"] = orm.relationship(back_populates="messages")
