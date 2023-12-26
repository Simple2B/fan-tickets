from typing import TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid, utcnow


if TYPE_CHECKING:
    from .user import User
    from .ticket import Ticket


class Dispute(db.Model, ModelMixin):
    ___tablename__ = "disputes"

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
        nullable=False,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=utcnow,
    )
    is_active: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        default=True,
    )
    buyer_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id"),
        nullable=False,
    )
    ticket_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("tickets.id"),
        nullable=False,
    )
    buyer: orm.Mapped["User"] = orm.relationship()
    ticket: orm.Mapped["Ticket"] = orm.relationship()

    # TODO: add seller, room, attachments (later)
