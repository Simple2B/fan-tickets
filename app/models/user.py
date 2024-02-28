from typing import TYPE_CHECKING
from enum import Enum
from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin


from app.database import db
from app.logger import log
from app import schema as s

from .users_events import users_events
from .user_notification import UserNotification
from .utils import ModelMixin, utcnow, gen_uuid

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
    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=gen_uuid)
    # Foreign keys
    identity_document_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("pictures.id"))
    picture_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("pictures.id"))
    last_notification_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("notifications.id"))
    # Columns
    username: orm.Mapped[str | None] = orm.mapped_column(sa.String(64))
    email: orm.Mapped[str] = orm.mapped_column(
        sa.String(256),
        unique=True,
        nullable=False,
    )
    name: orm.Mapped[str | None] = orm.mapped_column(sa.String(64))
    last_name: orm.Mapped[str | None] = orm.mapped_column(sa.String(64))
    phone: orm.Mapped[str | None] = orm.mapped_column(sa.String(32))
    address: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))
    birth_date: orm.Mapped[datetime | None] = orm.mapped_column(sa.DateTime)
    # Improve naming
    facebook: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))
    instagram: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))
    twitter: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))
    card: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))

    # Pagar.me
    document_identity_number: orm.Mapped[str | None] = orm.mapped_column(sa.String(32))
    pagarme_id: orm.Mapped[str | None] = orm.mapped_column(sa.String(32))

    # Pagar.me recipient data
    recipient_id: orm.Mapped[str | None] = orm.mapped_column(sa.String(32))
    bank: orm.Mapped[str | None] = orm.mapped_column(sa.String(4))
    branch_check_digit: orm.Mapped[str | None] = orm.mapped_column(sa.String(2))
    branch_number: orm.Mapped[str | None] = orm.mapped_column(sa.String(8))
    account_number: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))
    account_check_digit: orm.Mapped[str | None] = orm.mapped_column(sa.String(2))

    # Pagar.me card data
    card_id: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))
    billing_line_1: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))
    billing_line_2: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))
    billing_zip_code: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))
    billing_city: orm.Mapped[str | None] = orm.mapped_column(sa.String(64))
    billing_state: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))
    billing_country: orm.Mapped[str | None] = orm.mapped_column(sa.String(16))

    verification_code: orm.Mapped[str | None] = orm.mapped_column(sa.String(6))
    password_hash: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="")
    activated: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=utcnow,
    )
    reset_password_uuid: orm.Mapped[str] = orm.mapped_column(sa.String(64), default=gen_password_reset_id)
    role: orm.Mapped[str] = orm.mapped_column(sa.String(32), default=UserRole.client.value)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    # Individual financial settings
    service_fee: orm.Mapped[int | None] = orm.mapped_column(default=None, server_default=sa.text("NULL"))
    bank_fee: orm.Mapped[int | None] = orm.mapped_column(default=None, server_default=sa.text("NULL"))

    # Relationships
    identity_document: orm.Mapped["Picture"] = orm.relationship(foreign_keys=[identity_document_id])
    picture: orm.Mapped["Picture"] = orm.relationship(foreign_keys=[picture_id])
    tickets_for_sale: orm.Mapped[list["Ticket"]] = orm.relationship(
        foreign_keys="Ticket.seller_id", back_populates="seller"
    )
    tickets_bought: orm.Mapped[list["Ticket"]] = orm.relationship(
        foreign_keys="Ticket.buyer_id",
        back_populates="buyer",
    )
    notifications: orm.WriteOnlyMapped["Notification"] = orm.relationship(
        back_populates="users", secondary=UserNotification.__table__, passive_deletes=True
    )

    last_notification: orm.Mapped["Notification"] = orm.relationship(foreign_keys=[last_notification_id])
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
        self.reset_password_uuid = gen_password_reset_id()
        self.save()

    def __repr__(self):
        return f"<{self.id}: {self.username},{self.email}>"

    @property
    def json(self):
        u = s.User.model_validate(self)
        return u.model_dump_json()

    @property
    def birth_date_string(self):
        return self.birth_date.strftime("%m/%d/%Y") if self.birth_date else None

    @property
    def unread_notifications_count(self):
        session = orm.Session.object_session(self)

        assert session, "session is None in User.unread_notifications_count()"

        return session.scalar(
            sa.select(sa.func.count(UserNotification.notification_id)).where(
                UserNotification.user_id == self.id, UserNotification.is_viewed.is_(False)
            )
        )


class AnonymousUser(AnonymousUserMixin):
    pass
