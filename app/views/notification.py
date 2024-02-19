import sqlalchemy as sa

from http import HTTPStatus

from flask import render_template, Blueprint, request, abort
from flask_login import current_user, login_required

from app import models as m
from app.database import db


NOTIFICATIONS_PER_PAGE = 5

notification_blueprint = Blueprint("notification", __name__, url_prefix="/notification")


@notification_blueprint.route("/notifications", methods=["GET"])
@login_required
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
        "user/notification/notifications.html",
        notifications=notifications,
        page=page,
    )


@notification_blueprint.route("/", methods=["GET"])
@login_required
def notification_page():
    notifications_count = db.session.scalar(
        sa.select(sa.func.count(m.Notification.id)).where(m.Notification.users.any(m.User.id == current_user.id))
    )
    return render_template("user/notification/notification_page.html", notifications_count=notifications_count)


@notification_blueprint.route("/mark_as_read", methods=["GET"])
@login_required
def set_notification_is_viewed():
    notification_uuid = request.args.get("notification_uuid")

    if not notification_uuid:
        abort(HTTPStatus.BAD_REQUEST)

    notification = db.session.scalar(
        sa.select(m.Notification).where(
            m.Notification.uuid == notification_uuid, m.Notification.users.any(m.User.id == current_user.id)
        )
    )

    if not notification:
        abort(HTTPStatus.NOT_FOUND)

    notification.user_notification.is_viewed = True
    db.session.commit()

    return render_template("user/notification/notification.html", notification=notification)


@notification_blueprint.route("/get_unread_notifications", methods=["GET"])
@login_required
def get_unread_notifications():
    return str(current_user.unread_notifications_count), HTTPStatus.OK
