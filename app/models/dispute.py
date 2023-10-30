from datetime import datetime
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User
    from .ticket import Ticket


class Dispute(db.Model, ModelMixin):
    """
    Model for disputes
    """

    ___tablename__ = "disputes"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    buyer_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey(User.id),
        nullable=False,
    )
    description: orm.Mapped[str] = orm.mapped_column(
        sa.String(512),
        nullable=False,
    )
    ticket_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey(Ticket.id),
        nullable=False,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )
    is_active: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        default=True,
    )
