from flask import request, Blueprint, render_template
from flask_login import login_user

from app import controllers as c
from app import schema as s
from app import db
from app import forms as f
from app.logger import log
from config import config

CFG = config()

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/login_email")
def login_email():
    try:
        params = s.ChatAuthEmailParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.room_unique_id:
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

    if params.from_sign_up:
        c.save_message("You do not log in. Please log in or sign up", "Sign in", room)
        log(log.INFO, "Sign in from login form")
        return render_template(
            "chat/registration/login_email.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.user_message:
        log(log.ERROR, "No email: [%s]", params.user_message)
        return render_template(
            "chat/registration/login_email.html",
            error_message="Please, add your email",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    user = c.get_user_by_email(params.user_message, room)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_message)
        return render_template(
            "chat/registration/login_email.html",
            error_message="Email not found, add correct email or sign up",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    return render_template(
        "chat/registration/login_password.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.uuid,
        form=f.ChatAuthPasswordForm(),
        ticket_unique_id=params.ticket_unique_id,
    )


@auth_blueprint.route("/login_password", methods=["GET", "POST"])
def login_password():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error: [%s]",
            form.errors,
        )
        return render_template(
            "chat/registration/login_password.html",
            error_message=f"{form.errors}",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            ticket_unique_id=form.ticket_unique_id.data,
            form=form,
        )

    result, user = c.confirm_password(form, room)

    if not result:
        c.save_message("Please enter your password", "Password does not match", room)
        log(log.ERROR, "Password not confirmed: [%s]", form.password.data)
        return render_template(
            "chat/registration/password_confirm.html",
            error_message="Password does not match. Please, inout correct password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            ticket_unique_id=form.ticket_unique_id.data,
            form=form,
        )

    login_user(user)
    log(log.INFO, "Login successful")

    c.save_message("Please enter your password", "You are logged in", room)

    if form.ticket_unique_id.data:
        return render_template(
            "chat/buy/booking_ticket_from_web.html",
            now=c.utcnow_chat_format(),
            room=room,
            ticket_unique_id=form.ticket_unique_id.data,
        )

    return render_template(
        "chat/chat_home.html",
        now=c.utcnow_chat_format(),
        room=room,
    )


@auth_blueprint.route("/reset_registration", methods=["GET"])
def reset_registration():
    params = s.ChatAuthParams.model_validate(dict(request.args))

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        return render_template(
            "chat/email.html",
            now=c.utcnow_chat_format(),
            room=room,
        )

    db.session.delete(user)
    db.session.commit()

    return render_template(
        "chat/registration/email.html",
        now=c.utcnow_chat_format(),
        room=room,
    )
