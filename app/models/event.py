from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .location import Location
    from .ticket import Ticket


class Event(db.Model, ModelMixin):
    """
    Model for events

    Actions in admin section:
    - create
    - read
    - update
    - delete
    - set a foreign key from events to locations
    - set a foreign key from events to categories
    - set a foreign key from tickets to events

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

    image: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary, nullable=False)

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
    tickets: orm.Mapped[list["Ticket"]] = orm.relationship(
        "Ticket",
        back_populates="event",
    )
