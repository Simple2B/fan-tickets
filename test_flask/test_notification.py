from http import HTTPStatus

from flask.testing import FlaskClient

import sqlalchemy as sa

from app.database import db
from app import models as m
from app import flask_sse_notification
from app.controllers.notification_client import NotificationType

from .utils import login, TEST_ADMIN_EMAIL


def test_get_notifications(client: FlaskClient):
    login(client)

    flask_sse_notification.notify_admin({"username": "test_user"}, db.session, NotificationType.NEW_REGISTRATION)

    notification = db.session.scalar(
        sa.select(m.Notification).where(m.Notification.users.any(m.User.email == TEST_ADMIN_EMAIL))
    )
    assert notification

    response = client.get("admin/notification/get_notification")
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.get("admin/notification/get_notification?notification_uuid=abcdf")
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.get(f"admin/notification/get_notification?notification_uuid={notification.uuid}")
    assert response.status_code == HTTPStatus.OK
    assert "test_user" in response.text
