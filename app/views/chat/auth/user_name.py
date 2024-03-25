from sqlalchemy.exc import IntegrityError

from flask import request, Blueprint, render_template

from app import controllers as c
from app import schema as s
from app import db
from app.logger import log
from config import config

CFG = config()

user_name_blueprint = Blueprint("user_name", __name__, url_prefix="/user_name")


@user_name_blueprint.route("/create_first_name")
def create_first_name():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No name provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/name.html",
            error_message="Please, add your name",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    c.create_user_name(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "User name added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User name is not added: [%s]", e)
        return render_template(
            "chat/registration/name.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    return render_template(
        "chat/registration/last_name.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )


@user_name_blueprint.route("/create_last_name")
def create_last_name():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No last name provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/last_name.html",
            error_message="Please, add your last name",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if user.last_name:
        return render_template(
            "chat/registration/phone.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    c.create_user_last_name(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "User last name added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User last name is not added: [%s]", e)
        return render_template(
            "chat/registration/last_name.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    return render_template(
        "chat/registration/phone.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )
