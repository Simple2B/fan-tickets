import sqlalchemy as sa
from app.database import db

UserNotification = sa.Table(
    "user_notification",
    db.metadata,
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id"),
        primary_key=True,
    ),
    sa.Column(
        "notification_id",
        sa.Integer,
        sa.ForeignKey("notifications.id"),
        primary_key=True,
    ),
)
