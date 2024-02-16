from datetime import datetime
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

    users: orm.WriteOnlyMapped["User"] = orm.relationship(
        back_populates="notifications",
        secondary=UserNotification.__table__,
        passive_deletes=True,
        cascade="all, delete",
    )
    user_notification: orm.Mapped[UserNotification] = orm.relationship(viewonly=True)

    @property
    def is_viewed(self) -> bool:
        return self.user_notification.is_viewed

    def __repr__(self):
        return f"<{self.id}: {self.notification_type}>"
