import sqlalchemy as sa

from http import HTTPStatus

from flask import render_template, Blueprint, request, abort
from flask_login import current_user

from app import models as m
from app.database import db


NOTIFICATIONS_PER_PAGE = 5

notification_blueprint_admin = Blueprint("notification", __name__, url_prefix="/notification")


@notification_blueprint_admin.route("/", methods=["GET"])
def get_notifications():
    page = request.args.get("page", 1, type=int)
    total_notifications_count = db.session.scalar(
        sa.select(sa.func.count(m.Notification.id)).where(m.Notification.users.any(m.User.id == current_user.id))
    )
    total_pages = total_notifications_count // NOTIFICATIONS_PER_PAGE
    if page > total_pages + 1:
        return ""

    notifications = db.session.scalars(
        m.utils.generate_paginate_query(
            current_user.notifications.select().order_by(m.Notification.created_at.desc()),
            page,
            NOTIFICATIONS_PER_PAGE,
        )
    )

    return render_template(
        "notification/notifications.html",
        notifications=reversed(notifications.all()),
        page=page,
    )


@notification_blueprint_admin.route("/get_notification", methods=["GET"])
def get_notification():
    notification_uuid = request.args.get("notification_uuid")

    if not notification_uuid:
        abort(HTTPStatus.NOT_FOUND)

    where_stmt = [m.Notification.uuid == notification_uuid]

    notification = db.session.scalar(sa.select(m.Notification).where(*where_stmt))

    if not notification:
        abort(HTTPStatus.NOT_FOUND)

    return render_template("notification/notification.html", notification=notification)
