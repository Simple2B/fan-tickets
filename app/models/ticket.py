from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .location import Location


class Ticket(db.Model, ModelMixin):
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

    - quantity, original value, sales value
    - observations/conditions
    - read ticket barcode / QRcode
    - insert warning
    - net amount (price)
    - the amount the buyer should pay
    """

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=False,
        nullable=False,
    )
    image: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary, nullable=False)

    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("categories.id"), nullable=True
    )
    category: orm.Mapped[Category] = orm.relationship("Category", backref="events")

    location_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("categories.id"), nullable=True
    )
    location: orm.Mapped["Location"] = orm.relationship("Location", backref="events")

    creator_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=True
    )
    creator: orm.Mapped["User"] = orm.relationship("User", backref="events")
