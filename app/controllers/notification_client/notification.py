from typing import Iterable
from enum import Enum
from abc import ABC
from pydantic import BaseModel, Field

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


class NotificationData(BaseModel):
    uuid: str = Field(default_factory=m.gen_uuid)
    payload: dict = {}


class NotificationClient(ABC):
    def send_notification(self, data: dict | str, channel: str, notification_type: NotificationType):
        ...

    def notify_user(
        self,
        user: m.User,
        payload: dict,
        notification_type: NotificationType,
        session: orm.Session,
    ):
        self.notify_users((user,), payload, session, notification_type)

    def notify_users(
        self, users: Iterable[m.User], payload: dict, session: orm.Session, notification_type: NotificationType
    ):
        notification = m.Notification(
            users=users,
            payload=payload,
            notification_type=notification_type.value,
        )
        session.add(notification)
        session.commit()

        notification_text = NotificationData(payload=payload, uuid=notification.uuid)

        for user in users:
            self.send_notification(notification_text.model_dump(), f"notification:{user.uuid}", notification_type)

    def notify_admin(self, payload: dict | str, session: orm.Session, notification_type: NotificationType):
        notification = m.Notification(
            payload=payload if isinstance(payload, dict) else {"data": payload},
            notification_type=notification_type.value,
        )

        session.add(notification)
        session.commit()

        self.send_notification(
            NotificationData(payload=payload, uuid=notification.uuid).model_dump(), "admin", notification_type
        )
