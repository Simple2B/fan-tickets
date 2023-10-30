from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


class Dispute(db.Model, ModelMixin):
    """
    Model for disputes between buyers and sellers.

    Routes:
    - POST /disputes/create (user)
    - GET /admin/disputes (admin)
    - GET /admin/disputes/{dispute_unique_id} (admin)
    - GET /disputes/by_user/{user_unique_id} (admin, ajax sort)
    - GET /disputes/by_event/{event_unique_id} (admin, ajax sort)
    - GET /disputes/by_ticket/{ticket_unique_id} (admin, ajax sort)
    - PUT /admin/disputes/update/{dispute_unique_id} (admin)

    """

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
        default=datetime.utcnow,
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
