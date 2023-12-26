from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User


class NotificationsConfig(db.Model, ModelMixin):
    """
    Model for sending notifications to users
    User have to select in settings which notifications he wants to receive
    """

    __tablename__ = "notifications_configs"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))

    user: orm.Mapped["User"] = orm.relationship(
        back_populates="notifications_config",
    )
    new_event: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    new_ticket: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    new_message: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    new_buyers_payment: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    ticket_transfer_confirmed: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    your_payment_received: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    dispute_started: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    dispute_resolved: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)

    def __repr__(self):
        return f"<{self.id}: {self.user}>"
