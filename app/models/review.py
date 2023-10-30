from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


if TYPE_CHECKING:
    from .user import User


class Review(db.Model, ModelMixin):
    """
    Model for clients' reviews

    A review is supposed to be added from both:
    seller and buyer to each other and not supposed to be updated.

    Routes:
    - POST /reviews/create
    - GET /reviews
    - GET /reviews/{reviewer_unique_id}/{receiver_unique_id}
    - GET /reviews/{review_unique_id}
    - GET /reviews/made/{reviewer_unique_id}
    - GET /reviews/received/{receiver_unique_id}
    - DELETE /reviews/delete/{review_unique_id}
    - DELETE /reviews/delete_by_user/{user_unique_id}

    """

    __tablename__ = "reviews"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
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
