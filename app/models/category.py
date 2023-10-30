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

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    image: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary, nullable=False)
