from datetime import datetime
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app import schema as s
from app.database import db
from .utils import ModelMixin, gen_uuid
from .users_events import users_events


if TYPE_CHECKING:
    from .picture import Picture
    from .user import User
    from .category import Category
    from .location import Location
    from .ticket import Ticket


class Event(db.Model, ModelMixin):
    __tablename__ = "events"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64))

    picture_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("pictures.id"))

    url: orm.Mapped[str | None] = orm.mapped_column(
        sa.String(256),
    )

    observations: orm.Mapped[str | None] = orm.mapped_column(sa.String(512))
    warning: orm.Mapped[str | None] = orm.mapped_column()
    date_time: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True))
    approved: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    category_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("categories.id"))

    location_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("locations.id"))

    creator_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))

    location: orm.Mapped["Location"] = orm.relationship()
    category: orm.Mapped["Category"] = orm.relationship()
    creator: orm.Mapped["User"] = orm.relationship()
    tickets: orm.Mapped[list["Ticket"]] = orm.relationship(back_populates="event")
    picture: orm.Mapped["Picture"] = orm.relationship()
    subscribers: orm.Mapped[list["User"]] = orm.relationship(
        secondary=users_events,
        back_populates="subscribed_events",
    )

    @property
    def json(self):
        event = s.Event.model_validate(self)
        return event.model_dump_json()

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
