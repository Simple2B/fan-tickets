from sqlalchemy.exc import IntegrityError

from flask import request, Blueprint, render_template

from app import controllers as c
from app import schema as s
from app import forms as f
from app import db
from app.logger import log
from app import mail_controller
from config import config

CFG = config()

user_email_blueprint = Blueprint("user_email", __name__, url_prefix="/user_email")


@user_email_blueprint.route("/create")
def create():
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
        c.save_message("You do not log in. Please log in or sign up", "Sign up", room)
        log(log.INFO, "Sign up from selling")
        return render_template(
            "chat/registration/email.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.user_message:
        log(log.ERROR, "No email: [%s]", params.user_message)
        return render_template(
            "chat/registration/email.html",
            error_message="Field is empty",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    response, user = c.create_email(params.user_message, room)

    if response.is_error:
        return render_template(
            "chat/registration/email.html",
            error_message=response.message,
            room=room,
            now=c.utcnow_chat_format(),
            email_input=response.email,
            ticket_unique_id=params.ticket_unique_id,
        )

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_message)
        return render_template(
            "chat/registration/email.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    try:
        db.session.commit()
        log(log.INFO, f"User {user.email} created")
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User is not created: [%s]", e)
        return render_template(
            "chat/registration/email.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    mail_controller.send_email(
        (user,),
        f"Verify email for {CFG.APP_NAME}",
        render_template(
            "email/email_confirm.htm",
            verification_code=response.verification_code,
        ),
    )

    return render_template(
        "chat/registration/email_confirm.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.uuid,
        ticket_unique_id=params.ticket_unique_id,
    )


@user_email_blueprint.route("/verification")
def verification():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()

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
        log(log.ERROR, "No verification code: [%s]", params.user_message)
        return render_template(
            "chat/registration/email_confirm.html",
            error_message="No verification code, please confirm your email",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            form=form,
            ticket_unique_id=params.ticket_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if user.verification_code != params.user_message:
        log(log.ERROR, "Wrong verification code: [%s]", params.user_message)
        return render_template(
            "chat/registration/email_confirm.html",
            error_message="Wrong verification code, please confirm your email",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            form=form,
            ticket_unique_id=params.ticket_unique_id,
        )

    c.save_message("Please confirm your email", "Email confirmed", room)

    return render_template(
        "chat/registration/password.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.uuid,
        form=form,
        ticket_unique_id=params.ticket_unique_id,
    )
