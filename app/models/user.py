from datetime import datetime
from uuid import uuid4
from typing import TYPE_CHECKING
from flask_login import UserMixin, AnonymousUserMixin
import sqlalchemy as sa
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .users_events import users_events


from enum import Enum
from app.database import db
from .utils import ModelMixin
from app.logger import log
from app import schema as s


if TYPE_CHECKING:
    from .picture import Picture
    from .ticket import Ticket
    from .notification import Notification
    from .review import Review
    from .room import Room
    from .event import Event
    from .notifications_config import NotificationsConfig


class UserRole(Enum):
    admin = "admin"
    client = "client"


def gen_password_reset_id() -> str:
    return str(uuid4())


class User(db.Model, UserMixin, ModelMixin):
    __tablename__ = "users"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    email: orm.Mapped[str] = orm.mapped_column(sa.String(256))
    phone: orm.Mapped[str | None] = orm.mapped_column(sa.String(32))
    card: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))
    verification_code: orm.Mapped[str | None] = orm.mapped_column(sa.String(6))
    password_hash: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="")
    activated: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_password_reset_id,
    )
    reset_password_uid: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        default=gen_password_reset_id,
    )
    role: orm.Mapped[str] = orm.mapped_column(sa.String(32), default=UserRole.client.value)
    picture_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("pictures.id"))

    picture: orm.Mapped["Picture"] = orm.relationship()
    tickets_for_sale: orm.Mapped[list["Ticket"]] = orm.relationship(
        foreign_keys="Ticket.seller_id",
        back_populates="seller",
    )
    tickets_bought: orm.Mapped[list["Ticket"]] = orm.relationship(
        foreign_keys="Ticket.buyer_id",
        back_populates="buyer",
    )
    notifications: orm.Mapped[list["Notification"]] = orm.relationship(
        back_populates="user",
    )

    notifications_config: orm.Mapped["NotificationsConfig"] = orm.relationship(back_populates="user")

    reviewers: orm.Mapped[list["Review"]] = orm.relationship(
        foreign_keys="Review.reviewer_id",
        back_populates="reviewer",
    )

    receivers: orm.Mapped[list["Review"]] = orm.relationship(
        foreign_keys="Review.receiver_id",
        back_populates="receiver",
    )

    seller_chat_rooms: orm.Mapped[list["Room"]] = orm.relationship(
        foreign_keys="Room.seller_id",
        back_populates="seller",
    )
    buyer_chat_rooms: orm.Mapped[list["Room"]] = orm.relationship(
        foreign_keys="Room.buyer_id",
        back_populates="buyer",
    )
    subscribed_events: orm.Mapped[list["Event"]] = orm.relationship(
        secondary=users_events,
        back_populates="subscribers",
    )
    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(
        cls,
        user_id,
        password,
        session: orm.Session | None = None,
    ):
        if not session:
            session = db.session
        query = cls.select().where(
            (sa.func.lower(cls.username) == sa.func.lower(user_id))
            | (sa.func.lower(cls.email) == sa.func.lower(user_id))
        )
        assert session
        user = session.scalar(query)
        if not user:
            log(log.WARNING, "user:[%s] not found", user_id)

        if user is not None and check_password_hash(user.password, password):
            return user

    def reset_password(self):
        self.password_hash = ""
        self.reset_password_uid = gen_password_reset_id()
        self.save()

    def __repr__(self):
        return f"<{self.id}: {self.username},{self.email}>"

    @property
    def json(self):
        u = s.User.model_validate(self)
        return u.model_dump_json()


class AnonymousUser(AnonymousUserMixin):
    pass
