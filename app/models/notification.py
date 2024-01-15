from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid, utcnow

from .user_notification import UserNotification


if TYPE_CHECKING:
    from .user import User


class Notification(db.Model, ModelMixin):
    __tablename__ = "notifications"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=utcnow,
    )
    notification_type: orm.Mapped[str] = orm.mapped_column(sa.String(32))
    payload: orm.Mapped[dict] = orm.mapped_column(sa.JSON, default={})

    is_viewed: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    users: orm.WriteOnlyMapped["User"] = orm.relationship(
        back_populates="notifications",
        secondary=UserNotification,
    )

    def __repr__(self):
        return f"<{self.id}: {self.notification_type}>"
