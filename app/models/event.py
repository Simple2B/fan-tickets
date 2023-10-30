from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .location import Location


class Event(db.Model, ModelMixin):

    __tablename__ = "events"
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
    """

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
    # event_type: orm.Mapped[str] = orm.mapped_column(
    #     sa.String(32), default=EventType.BOX.value
    # )
    date_time: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        nullable=False,
    )

    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey(Category.id), nullable=True
    )

    location_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey(Location.id), nullable=True
    )

    creator_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey(User.id), nullable=True
    )

    location: orm.Mapped["Location"] = orm.relationship(backref="events")
    category: orm.Mapped["Category"] = orm.relationship(backref="events")
    creator: orm.Mapped["User"] = orm.relationship(backref="events")
