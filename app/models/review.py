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
    - GET /reviews/{reviewer_unique_id}/{receiver_unique_id} - do not need this
    - GET /reviews/{review_unique_id} - do not need this
    - GET /reviews/made/{reviewer_unique_id} - do not need this
    - GET /reviews/received/{receiver_unique_id} - do not need this
    - DELETE /reviews/delete/{review_unique_id}  (admin)
    - DELETE /reviews/delete_by_user/{user_unique_id} (admin, ajax sort)

    """

    __tablename__ = "reviews"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )

    rate: orm.Mapped[int | None] = orm.mapped_column()
    text: orm.Mapped[str | None] = orm.mapped_column(sa.String(512))

    reviewer_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))
    receiver_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"))

    reviewer: orm.Mapped["User"] = orm.relationship(
        foreign_keys=[reviewer_id],
        back_populates="reviewers",
    )

    receiver: orm.Mapped["User"] = orm.relationship(
        foreign_keys=[receiver_id],
        back_populates="receivers",
    )

    def __repr__(self):
        return f"<{self.id}: {self.reviewer} - {self.receiver}>"
