import sqlalchemy as sa
from app.database import db


users_tickets = sa.Table(
    "users_tickets",
    db.Model.metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("ticket_id", sa.Integer, sa.ForeignKey("tickets.id")),
)
