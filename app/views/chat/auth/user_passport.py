from flask import request, Blueprint, render_template

from app import controllers as c
from app import schema as s
from app import forms as f
from app.logger import log
from config import config

CFG = config()

user_passport_blueprint = Blueprint("user_passport", __name__, url_prefix="/user_passport")


@user_passport_blueprint.route("/upload", methods=["GET", "POST"])
def upload():
    form: f.ChatFileUploadForm = f.ChatFileUploadForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        log(log.ERROR, "Room not found: [%s]", form.room_unique_id.data)
        return render_template(
            "chat/sell/passport.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error, user_unique_id: [%s], room_unique_id: [%s]",
            form.user_unique_id.data,
            form.room_unique_id.data,
        )
        return render_template(
            "chat/registration/passport.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    if not form.file.data:
        log(log.ERROR, "No identification document: [%s]", form.file.data)
        return render_template(
            "chat/registration/passport.html",
            error_message="No verification document, please upload your identification document",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    user = c.get_user(form.user_unique_id.data)

    if not user:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )
    if user.identity_document:
        return render_template(
            "chat/registration/passport_identity_number.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    error_message = c.add_identity_document(form, room)

    if error_message:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/passport.html",
            error_message=error_message,
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    return render_template(
        "chat/registration/passport_identity_number.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=form.user_unique_id.data,
        form=form,
    )


@user_passport_blueprint.route("/create")
def create():
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
        log(log.ERROR, "No identity number provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/passport_identity_number.html",
            error_message="Please, add your CPF number",
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

    if user.document_identity_number:
        c.save_message("Please input your CPF number", f"CPF number: {params.user_message}", room)
        return render_template(
            "chat/registration/name.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    c.add_identity_document_number(params.user_message, user, room)

    return render_template(
        "chat/registration/name.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )
