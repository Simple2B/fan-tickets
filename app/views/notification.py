import sqlalchemy as sa

from http import HTTPStatus

from flask import render_template, Blueprint, request, abort
from flask_login import current_user, login_required

from app import models as m
from app.database import db


NOTIFICATIONS_PER_PAGE = 5

notification_blueprint = Blueprint("notification", __name__, url_prefix="/notification")


@notification_blueprint.route("/", methods=["GET"])
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
        "notification/notifications.html",
        notifications=notifications,
        page=page,
    )


@notification_blueprint.route("/notification_list", methods=["GET"])
@login_required
def notification_list():
    notifications_count = db.session.scalar(
        sa.select(sa.func.count(m.Notification.id)).where(m.Notification.users.any(m.User.id == current_user.id))
    )
    return render_template("user/notification/notifications.html", notifications_count=notifications_count)
