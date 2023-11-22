import sqlalchemy as sa
from app.database import db


users_events = sa.Table(
    "users_events",
    db.Model.metadata,
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("event_id", sa.ForeignKey("events.id"), primary_key=True),
)
