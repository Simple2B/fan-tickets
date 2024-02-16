from typing import Iterable
from enum import Enum
from abc import ABC
from pydantic import BaseModel, Field

import sqlalchemy as sa
from sqlalchemy import orm

from app import models as m


class NotificationType(Enum):
    NEW_REGISTRATION = "new_registration"
    NEW_POST = "new_post"
    ACCOUNT_VERIFIED = "account_verified"
    TICKET_PUBLISHED = "ticket_published"
    TICKET_AVAILABLE = "ticket_available"
    TICKET_SOLD = "ticket_sold"
    PAYMENT_APPROVED = "payment_approved"
    DISPUTE_CREATED = "dispute_created"
    DISPUTE_NEW_MESSAGE = "dispute_new_message"


class NotificationData(BaseModel):
    uuid: str = Field(default_factory=m.gen_uuid)
    payload: dict | str = {}


class NotificationClient(ABC):
    def send_notification(
        self,
        data: dict,
        channel: str,
    ):
        ...

    def notify_users(
        self,
        users: Iterable[m.User],
        payload: dict,
        session: orm.Session,
        notification_type: NotificationType,
    ):
        # save notification in database
        for user in users:
            notification = m.Notification(
                users=[user],
                payload=payload,
                notification_type=notification_type.value,
            )
            session.add(notification)
        session.commit()
        # send sse notification
        for user in users:
            self.send_notification(payload, f"notification:{user.uuid}")

    def notify_room(self, room: m.Room, payload: dict):
        self.send_notification(payload, f"room:{room.unique_id}")

    def notify_admin(self, payload: dict, session: orm.Session, notification_type: NotificationType):
        admin_users = session.scalars(sa.select(m.User).where(m.User.role == m.UserRole.admin.value))
        notification = m.Notification(
            payload=payload,
            notification_type=notification_type.value,
            users=admin_users,
        )

        session.add(notification)
        session.commit()

        self.send_notification(NotificationData(payload=payload, uuid=notification.uuid).model_dump(), "admin")
