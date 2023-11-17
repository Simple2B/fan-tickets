from datetime import datetime
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


if TYPE_CHECKING:
    from .user import User
    from .room import Room


class Message(db.Model, ModelMixin):
    """
    Model for chat or dispute messages.

    Routes:
    # - GET /messages/room/{room_unique_id}/ - do not need this
    - POST /messages/room/{room_unique_id}/ (admin/client)
    - PUT /messages/update/{message_unique_id} (admin/client)
    - DELETE /messages/delete/{message_unique_id} (admin/client)
    """

    __tablename__ = "messages"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
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
        sa.Text,
        nullable=False,
    )

    sender: orm.Mapped["User"] = orm.relationship()
    room: orm.Mapped["Room"] = orm.relationship(back_populates="messages")

    def __repr__(self):
        return f"<{self.id}: {self.text[:7]}>"
