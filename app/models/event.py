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
    """
    Model for events

    Questions:
    - observations/conditions
    - insert warning

    Routes:
    - POST /events/create (admin/user)
    - GET /events
    - GET /events/{event_unique_id}
    - GET /events/by_location/{location_unique_id} (client, ajax sort)
    - PUT /events/update/{event_unique_id} (admin)
    - DELETE /events/delete/{event_unique_id} (admin)

    Notice that on the event page there should be a swithcer to show/hide tickets

    """

    __tablename__ = "events"

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
        unique=False,
        nullable=False,
    )

    picture_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("pictures.id"), nullable=True
    )

    url: orm.Mapped[str] = orm.mapped_column(
        sa.String(255),
        unique=False,
        nullable=True,
    )

    observations: orm.Mapped[str] = orm.mapped_column(
        sa.String(512),
        unique=False,
        nullable=True,
    )
    warning: orm.Mapped[str] = orm.mapped_column(
        sa.String(512), unique=False, nullable=True
    )
    date_time: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
    )

    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("categories.id"), nullable=True
    )

    location_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("locations.id"), nullable=True
    )

    creator_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=True
    )

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
