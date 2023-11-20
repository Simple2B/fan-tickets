from typing import TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


if TYPE_CHECKING:
    from .picture import Picture


class Category(db.Model, ModelMixin):

    """
    Model for categories of events

    Actions in admin section:
    - create
    - read
    - update
    - delete
    - set a foreign key from events to categories

    Routes:
    - POST /admin/categories/create (admin)
    - GET /admin/categories (admin/user)
    - GET /admin/categories/{category_unique_id} (admin, ajax)
    - PUT /admin/categories/update/{category_unique_id} (admin, ajax)
    - DELETE /admin/categories/delete/{category_unique_id} (admin, ajax)

    """

    __tablename__ = "categories"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        nullable=False,
    )
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    picture_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("pictures.id"), nullable=True
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), default=datetime.utcnow
    )

    picture: orm.Mapped["Picture"] = orm.relationship()

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
