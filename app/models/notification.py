from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


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
    __tablename__ = "notifications"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
    )
    type_of: orm.Mapped[str] = orm.mapped_column(sa.String(32), default=NotificationType.TICKET_PUBLISHED.value)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))
    text: orm.Mapped[str] = orm.mapped_column(
        sa.String(512),
    )
    is_viewed: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    user: orm.Mapped["User"] = orm.relationship(
        back_populates="notifications",
    )

    def __repr__(self):
        return f"<{self.id}: {self.type_of}>"
