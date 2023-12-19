from datetime import datetime
from flask import request, render_template, current_app as app
from app import schema as s
from app import models as m, db
from app.logger import log


def check_user_room_id(template: str):
    """
    The function for uploading an image to the server.
    It is supposed to be universal for all models that have a picture.
    In case if we have to save an image as a user's profile picture,
    we pass the user as an argument.

    In future, we can add different instance (location, event) as an argument and save the image.

    At the moment it returns an empty dict and 200 status code if picture is uploaded and saved.

    Currently the default format of the image is PNG.
    """
    params = s.ChatAuthParams.model_validate(request.args)

    now = datetime.now()
    now_str = now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])

    room_query = m.Room.select().where(m.Room.unique_id == params.room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            template,
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    if not params.room_unique_id or not params.user_unique_id:
        log(
            log.ERROR,
            "Form submitting error, user_unique_id: [%s], room_unique_id: [%s]",
            params.user_unique_id,
            params.room_unique_id,
        )
        return render_template(
            template,
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    user_query = m.User.select().where(m.User.unique_id == params.user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            template,
            error_message="Form submitting error",
            room=room,
            now=now_str,
            user_unique_id=params.user_unique_id,
        )

    # TODO: make a pydantic model dict
    # result_dict = s.ChatAuthResultParams(user=user, room=room, now_str=now_str, params=params)
    # result = result_dict.model_dump()
    return params, user, room, now_str
