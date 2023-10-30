from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


class Location(db.Model, ModelMixin):
    __tablename__ = "locations"

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
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
