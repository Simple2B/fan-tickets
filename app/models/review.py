from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User


class Review(db.Model, ModelMixin):
    """
    Model for clients' reviews
    """

    __tablename__ = "reviews"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )

    rate: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        nullable=True,
    )
    text: orm.Mapped[str] = orm.mapped_column(sa.String(512), nullable=True)

    reviewer_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id"),
        nullable=False,
    )
    receiver_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("users.id"),
        nullable=False,
    )
    reviewer: orm.Mapped["User"] = orm.relationship(
        back_populates="reviews",
    )
    receiver: orm.Mapped["User"] = orm.relationship(
        back_populates="receivers",
    )
