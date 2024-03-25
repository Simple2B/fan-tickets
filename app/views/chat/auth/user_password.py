from sqlalchemy.exc import IntegrityError

from flask import Blueprint, render_template

from app import controllers as c
from app import forms as f
from app import models as m, db
from app.logger import log
from config import config

CFG = config()

user_password_blueprint = Blueprint("user_password", __name__, url_prefix="/user_password")


@user_password_blueprint.route("/create", methods=["POST"])
def create():
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
            "chat/registration/password.html",
            error_message="You did not add your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
            ticket_unique_id=form.ticket_unique_id.data,
        )

    success = c.create_password(form, room)

    try:
        db.session.commit()
        log(log.INFO, "User password added")
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User is not created: [%s]", e)
        return render_template(
            "chat/registration/password.html",
            error_message="Form submitting error. Please add your email again",
            user_unique_id=form.user_unique_id.data,
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not success:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/password.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
            ticket_unique_id=form.ticket_unique_id.data,
        )

    return render_template(
        "chat/registration/password_confirm.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=form.user_unique_id.data,
        form=form,
        ticket_unique_id=form.ticket_unique_id.data,
    )


@user_password_blueprint.route("/confirm", methods=["POST"])
def confirm():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()
    form_file = f.ChatFileUploadForm()

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
            "chat/registration/password_confirm.html",
            error_message="Please, confirm your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
            ticket_unique_id=form.ticket_unique_id.data,
        )

    result, user = c.confirm_password(form, room)

    if not result:
        c.save_message("Please confirm your password", "Password does not match", room)
        log(log.ERROR, "Password not confirmed: [%s]", form.password.data)
        return render_template(
            "chat/registration/password_confirm.html",
            error_message="Password does not match. Please, confirm your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
            ticket_unique_id=form.ticket_unique_id.data,
        )

    if form.ticket_unique_id.data:
        ticket_query = m.Ticket.select().where(m.Ticket.unique_id == form.ticket_unique_id.data)
        ticket: m.Ticket = db.session.scalar(ticket_query)
        room.ticket = ticket
        room.save()

    c.save_message("Please confirm your password", "Password has been confirmed", room)

    return render_template(
        "chat/registration/passport_identity_number.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=form.user_unique_id.data,
        form=form_file,
        ticket_unique_id=form.ticket_unique_id.data,
    )
