from datetime import datetime
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid, utcnow


if TYPE_CHECKING:
    from .user import User
    from .room import Room


class Message(db.Model, ModelMixin):
    """
    Model for chat or dispute messages.
    """

    __tablename__ = "messages"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )
    sender_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("users.id"))
    room_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("rooms.id"))
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=utcnow,
    )
    viewed: orm.Mapped[bool] = orm.mapped_column(default=False)
    text: orm.Mapped[str] = orm.mapped_column(sa.Text)

    sender: orm.Mapped["User"] = orm.relationship()
    room: orm.Mapped["Room"] = orm.relationship(back_populates="messages")

    def __repr__(self):
        return f"<{self.id}: {self.text[:7]}>"
