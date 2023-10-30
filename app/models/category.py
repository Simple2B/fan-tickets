from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


class Category(db.Model, ModelMixin):

    """
    Model for categories of events

    Actions in admin section:
    - create
    - read
    - update
    - delete
    - set a foreign key from events to categories
    """

    __tablename__ = "categories"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        nullable=False,
    )

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    image: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary, nullable=False)

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), default=datetime.utcnow
    )
