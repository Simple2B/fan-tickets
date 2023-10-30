import sqlalchemy as sa
from app.database import db


users_reviews = sa.Table(
    "users_reviews",
    db.Model.metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("review_id", sa.Integer, sa.ForeignKey("reviews.id")),
)
