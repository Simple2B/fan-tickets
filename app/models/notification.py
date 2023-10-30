from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User


class NotificationType(Enum):
    NEW_REGISTRATION = "new_registration"
    NEW_POST = "new_post"
    ACCOUNT_VERIFIED = "account_verified"
    TICKET_PUBLISHED = "ticket_published"
    TICKET_AVAILABLE = "ticket_available"
    TICKET_SOLD = "ticket_sold"
    PAYMENT_APPROVED = "payment_approved"
    DISPUTE_CREATED = "dispute_created"


class Notification(db.Model, ModelMixin):
    """
    Model for chat or dispute messages
    """

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
    )
    type_of: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), default=NotificationType.TICKET_PUBLISHED.value
    )
    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id"),
        nullable=False,
    )
    text: orm.Mapped[str] = orm.mapped_column(
        sa.String(512),
        unique=False,
        nullable=False,
    )
    is_viewed: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    user: orm.Mapped["User"] = orm.relationship(
        "User",
        back_populates="notifications",
    )
