from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .ticket import Ticket
    from .message import Message


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
    buyer_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey(Ticket.id),
        nullable=False,
    )
    buyer: orm.Mapped["Ticket"] = orm.relationship(
        "Ticket",
        back_populates="buyer",
    )

    seller_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey(Ticket.id),
        nullable=False,
    )
    seller: orm.Mapped["Ticket"] = orm.relationship(
        "Ticket",
        back_populates="seller",
    )

    # Rate of the seller
