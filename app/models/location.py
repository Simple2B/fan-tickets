from typing import TYPE_CHECKING
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid, utcnow


if TYPE_CHECKING:
    from .picture import Picture
    from .event import Event


class Location(db.Model, ModelMixin):
    __tablename__ = "locations"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64))
    picture_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("pictures.id"))
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=utcnow,
    )
    deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False, server_default=sa.text("false"))

    picture: orm.Mapped["Picture"] = orm.relationship()
    events: orm.Mapped[list["Event"]] = orm.relationship(back_populates="location")

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
