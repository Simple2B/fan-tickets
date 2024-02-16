import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db


class UserNotification(db.Model):
    __tablename__ = "user_notifications"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))
    notification_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("notifications.id", ondelete="CASCADE"))
    is_viewed: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
