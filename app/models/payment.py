from typing import TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User
    from .ticket import Ticket


class Payment(db.Model, ModelMixin):
    __tablename__ = "payments"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    buyer_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))
    ticket_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("tickets.id"))
    description: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )

    ticket: orm.Mapped["Ticket"] = orm.relationship()
    buyer: orm.Mapped["User"] = orm.relationship()

    def __repr__(self):
        return f"<{self.id}:<{self.ticket}>|<{self.buyer.username}"
