from flask import current_app as app
from app import models as m


def send_message(bot_message: str, user_message: str, room: m.Room):
    """
    The function for uploading an image to the server.
    It is supposed to be universal for all models that have a picture.
    In case if we have to save an image as a user's profile picture,
    we pass the user as an argument.

    In future, we can add different instance (location, event) as an argument and save the image.

    At the moment it returns an empty dict and 200 status code if picture is uploaded and saved.

    Currently the default format of the image is PNG.
    """
    m.Message(
        sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
        room_id=room.id,
        text=bot_message,
    ).save(False)
    m.Message(
        room_id=room.id,
        text=user_message,
    ).save()
