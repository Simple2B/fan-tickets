import os
from datetime import datetime
from urllib.parse import urlparse

from sqlalchemy.exc import IntegrityError

from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user

from app import controllers as c
from app import schema as s
from app import models as m, db
from app.logger import log
from app import mail_controller
from config import config

CFG = config()

user_second_data_blueprint = Blueprint("user_second_data", __name__)


@user_second_data_blueprint.route("/create_user_phone")
def create_user_phone():
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
            "chat/registration/phone.html",
            error_message="Please, add your phone",
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

    if user.phone:
        return render_template(
            "chat/registration/address.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    error_message = c.create_phone(params.user_message, user, room)

    if error_message:
        log(log.ERROR, error_message)
        return render_template(
            "chat/registration/phone.html",
            error_message=error_message,
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            phone=params.user_message,
        )

    try:
        db.session.commit()
        log(log.INFO, "Phone added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Phone is not added: [%s]", e)
        return render_template(
            "chat/registration/phone.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    if os.environ.get("APP_ENV") == "development":
        parsed_url = urlparse(request.base_url)
        profile_url = f"{parsed_url.scheme}://{parsed_url.netloc}/user/profile"
    else:
        if os.environ.get("SERVER_TYPE") == "production":
            base_url = app.config["PRODUCTION_BASE_URL"]
        else:
            base_url = app.config["STAGING_BASE_URL"]
        profile_url = f"{base_url}user/profile"

    return render_template(
        "chat/registration/address.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.uuid,
        profile_url=profile_url,
    )


@user_second_data_blueprint.route("/create_user_address")
def create_user_address():
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
        log(log.ERROR, "No address provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/address.html",
            error_message="Please, add your address",
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

    if user.address:
        return render_template(
            "chat/registration/birth_date.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    c.create_address(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "Address added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Address is not added: [%s]", e)
        return render_template(
            "chat/registration/address.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/registration/birth_date.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )


@user_second_data_blueprint.route("/create_user_birth_date")
def create_user_birth_date():
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
        log(log.ERROR, "No birth date provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/birth_date.html",
            error_message="Please, add your birth date",
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

    birth_date_added = c.create_birth_date(params.user_message, user, room)
    if not birth_date_added:
        log(log.ERROR, "Birth date not added: [%s]", params.user_message)
        return render_template(
            "chat/registration/birth_date.html",
            error_message="Wrong date format. Please try again",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    try:
        db.session.commit()
        log(log.INFO, "Birth date added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Birth date is not added: [%s]", e)
        return render_template(
            "chat/registration/birth_date.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if current_user.is_authenticated:
        messages_query = m.Message.select().where(m.Message.room_id == room.id)
        messages = db.session.scalars(messages_query).all()

        mail_controller.send_email(
            (current_user,),
            f"Today's chat history {datetime.now().strftime(app.config['DATE_CHAT_HISTORY_FORMAT'])}",
            render_template(
                "email/chat_history.htm",
                user=current_user,
                messages=messages,
            ),
        )
        for message in messages:
            db.session.delete(message)
        db.session.commit()

        return render_template(
            "chat/chat_home.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    return render_template(
        "chat/registration/ask_social_profile.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )
