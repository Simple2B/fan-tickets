from datetime import datetime
from uuid import uuid4
from typing import TYPE_CHECKING
from flask_login import UserMixin, AnonymousUserMixin
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from .users_tickets import users_tickets
from .users_reviews import users_reviews


from enum import Enum
from app.database import db
from .utils import ModelMixin
from app.logger import log
from app import schema as s


if TYPE_CHECKING:
    from .ticket import Ticket
    from .notification import Notification
    from .review import Review


class UserRole(Enum):
    admin = "admin"
    client = "client"


def gen_password_reset_id() -> str:
    return str(uuid4())


class User(db.Model, UserMixin, ModelMixin):
    """
    Questions:
    - how to verificate personal info from the admin side


    Routes:
    - POST /admin/users/create_admin (admin)
    - POST /admin/users/create_client  (admin)
    - GET /admin/users
    - GET /profile (client)
    - GET /users/{user_unique_id} (client)
    - GET /users/by_roles/{user_role} (admin, ajax sort)
    - PUT /users/update/{user_unique_id} (client)
    - PUT /users/email_change/{user_unique_id} (client)
    - PUT /users/person_verification/{user_unique_id} (client)
    - DELETE /users/delete/{user_unique_id} (admin)

    Auth routes are in views/auth.py

    """

    __tablename__ = "users"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    image: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary, nullable=True)
    email: orm.Mapped[str] = orm.mapped_column(
        sa.String(255),
        unique=True,
        nullable=False,
    )
    password_hash: orm.Mapped[str] = orm.mapped_column(sa.String(255), default="")
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

    role: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), default=UserRole.client.value
    )

    tickets_for_sale: orm.Mapped[list["Ticket"]] = orm.relationship(
        "Ticket",
        secondary=users_tickets,
        back_populates="seller",
    )
    tickets_bought: orm.Mapped[list["Ticket"]] = orm.relationship(
        "Ticket",
        secondary=users_tickets,
        back_populates="buyer",
    )
    notifications: orm.Mapped[list["Notification"]] = orm.relationship(
        "Notification",
        back_populates="user",
    )

    reviews: orm.Mapped[list["Review"]] = orm.relationship(
        secondary=users_reviews,
        back_populates="reviewer",
    )

    receivers: orm.Mapped[list["Review"]] = orm.relationship(
        secondary=users_reviews,
        back_populates="receiver",
    )

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, user_id, password):
        query = cls.select().where(
            (sa.func.lower(cls.username) == sa.func.lower(user_id))
            | (sa.func.lower(cls.email) == sa.func.lower(user_id))
        )
        user = db.session.scalar(query)
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
        u = s.User.from_orm(self)
        return u.json()


class AnonymousUser(AnonymousUserMixin):
    pass
