import sqlalchemy as sa

from http import HTTPStatus

from flask import request, Blueprint, render_template, current_app as app, abort, redirect, url_for, flash
from flask_login import current_user, login_required

from app import models as m, db
from app import flask_sse_notification
from app.controllers import NotificationType
from app.logger import log
from app import forms as f
from app import mail_controller
from config import config

CFG = config()

chat_disputes_blueprint = Blueprint("disputes", __name__, url_prefix="/disputes")

CHAT_MESSAGES_PER_PAGE = 5


@chat_disputes_blueprint.route("/", methods=["GET"])
def start_dispute():
    payment_id = request.args.get("payment_id")

    if not payment_id:
        abort(HTTPStatus.BAD_REQUEST)

    payment = db.session.scalar(sa.select(m.Payment).where(m.Payment.id == payment_id))

    if not payment:
        abort(HTTPStatus.NOT_FOUND)

    room = db.session.scalar(
        sa.select(m.Room).where(
            m.Room.ticket_id == payment.ticket_id,
            sa.or_(
                m.Room.seller_id == current_user.id,
                m.Room.buyer_id == current_user.id,
            ),
        )
    )

    if not room:
        log(log.INFO, "Creating dispute room for payment [%s]", payment.id)
        room = m.Room(
            type_of=m.RoomType.DISPUTE.value,
            seller=payment.ticket.seller,
            buyer=current_user,
            ticket=payment.ticket,
        )

        message = m.Message(
            sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
            text="If you want to start a dispute, please describe the issue",
        )
        room.messages.add(message)

        db.session.add(room)
        db.session.commit()

        # send admin notification
        flask_sse_notification.notify_admin(
            {"room_uuid": room.unique_id, "buyer": current_user.email, "seller": payment.ticket.seller.email},
            db.session,
            NotificationType.DISPUTE_CREATED,
        )
        # send rooms users
        flask_sse_notification.notify_users(
            (current_user, payment.ticket.seller),
            {
                "room_uuid": room.unique_id,
                "buyer": current_user.email,
                "seller": payment.ticket.seller.email,
                "event": payment.ticket.event.name,
            },
            db.session,
            NotificationType.DISPUTE_CREATED,
        )
        user: m.User = current_user
        recipients = []

        if user.notifications_config.dispute_started:
            recipients.append(user)
        if payment.ticket.seller.notifications_config.dispute_started:
            recipients.append(payment.ticket.seller)

        # send email notification (Admins + room users)
        admins = db.session.scalars(m.User.select().where(m.User.role == m.UserRole.admin.value)).all()
        mail_controller.send_email(
            admins + recipients,
            "Dispute created",
            render_template(
                "email/dispute_created.html",
                event_name=payment.ticket.event.name,
            ),
        )

    else:
        room.type_of = m.RoomType.DISPUTE.value
        room.save()
        log(log.INFO, "Dispute room already exists for payment [%s]", payment.id)

    room.is_open = True
    db.session.commit()

    return room.unique_id, HTTPStatus.OK


@chat_disputes_blueprint.route("/get_message", methods=["GET"])
@login_required
def get_message():
    message_uuid = request.args.get("message_uuid")

    if not message_uuid:
        abort(HTTPStatus.BAD_REQUEST)

    message_filter = [m.Message.unique_id == message_uuid]
    if not current_user.role == m.UserRole.admin.value:
        message_filter.append(
            sa.or_(
                m.Message.room.has(m.Room.buyer_id == current_user.id),
                m.Message.room.has(m.Room.seller_id == current_user.id),
            )
        )

    message = db.session.scalar(sa.select(m.Message).where(*message_filter))

    if not message:
        abort(HTTPStatus.NOT_FOUND)

    return render_template("chat/chat_dispute_message.html", message=message)


@chat_disputes_blueprint.route("/get_messages", methods=["GET"])
@login_required
def get_messages():
    page = request.args.get("page", 1, type=int)
    room_uuid = request.args.get("room_uuid")

    if not room_uuid:
        abort(HTTPStatus.CONFLICT)

    room_query = [m.Room.unique_id == room_uuid]
    if not current_user.role == m.UserRole.admin.value:
        room_query.append(
            sa.or_(
                m.Room.seller_id == current_user.id,
                m.Room.buyer_id == current_user.id,
            ),
        )

    room = db.session.scalar(
        sa.select(m.Room).where(
            *room_query,
        )
    )

    if not room:
        abort(HTTPStatus.NOT_FOUND)

    total_messages_count = db.session.scalar(
        sa.select(sa.func.count(m.Message.id)).where(m.Message.room.has(m.Room.id == room.id))
    )
    total_pages = total_messages_count // CHAT_MESSAGES_PER_PAGE
    if page > total_pages + 1:
        return ""

    messages = db.session.scalars(
        m.utils.generate_paginate_query(
            room.messages.select().order_by(m.Message.created_at.desc()),
            page,
            CHAT_MESSAGES_PER_PAGE,
        )
    )

    return render_template(
        "chat/chat_dispute_messages.html",
        messages=reversed(messages.all()),
        page=page,
        room=room,
    )


@chat_disputes_blueprint.route("/send", methods=["POST"])
@login_required
def send_message():
    form = f.MessageForm()
    if not form.validate_on_submit():
        abort(HTTPStatus.BAD_REQUEST)

    room: m.Room = db.session.scalar(m.Room.select().where(m.Room.unique_id == form.room_unique_id.data))

    if not room:
        abort(HTTPStatus.NOT_FOUND)

    message = m.Message(
        room_id=room.id,
        sender_id=current_user.id,
        text=form.message.data,
    )
    db.session.add(message)
    db.session.commit()

    users: tuple[m.User, ...]

    if current_user.id == room.seller_id:
        users = (room.buyer,)
    elif current_user.id == room.buyer_id:
        users = (room.seller,)
    else:
        users = (room.seller, room.buyer)

    flask_sse_notification.notify_users(
        users, {"room_uuid": room.unique_id, "from": current_user.name}, db.session, NotificationType.NEW_POST
    )
    flask_sse_notification.notify_room(room, {"msg": message.unique_id})

    return "OK", HTTPStatus.OK


@chat_disputes_blueprint.route("/close", methods=["GET"])
@login_required
def close_dispute():
    room_unique_id = request.args.get("room_unique_id")

    if not room_unique_id:
        log(log.ERROR, "No room_unique_id provided")
        flash("Something went wrong", "danger")
        return redirect(url_for("admin.get_disputes"))

    room = db.session.scalar(sa.select(m.Room).where(m.Room.unique_id == room_unique_id))

    if not room:
        log(log.ERROR, "Room [%s] not found", room_unique_id)
        flash("Something went wrong", "danger")

    if not room.is_open:
        log(log.ERROR, "Room [%s] already closed", room_unique_id)
        flash("Dispute already closed", "danger")
        return redirect(url_for("admin.get_disputes"))

    room.is_open = False
    db.session.commit()

    recipients = []

    if room.seller.notifications_config.dispute_resolved:
        recipients.append(room.seller)
    if room.buyer.notifications_config.dispute_resolved:
        recipients.append(room.buyer)

    # send email notification
    admins = db.session.scalars(m.User.select().where(m.User.role == m.UserRole.admin.value)).all()
    mail_controller.send_email(
        admins + recipients,
        "Dispute closed",
        render_template(
            "email/dispute_closed.html",
            event_name=room.ticket.event.name,
        ),
    )

    log(log.INFO, "Dispute closed room: [%s]", room)
    flash("Dispute closed", "success")
    return redirect(url_for("admin.get_disputes"))
