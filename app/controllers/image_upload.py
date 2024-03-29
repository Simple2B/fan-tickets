import io
from enum import Enum
from PIL import Image
from flask import request, flash, current_app as app
from app import models as m
from app.database import db
from app.logger import log


class ImageType(Enum):
    LOGO = "logo"
    IDENTIFICATION = "identification"
    EVENT = "event"


def image_upload(user: m.User, image_type: ImageType):
    """
    The function for uploading an image to the server.
    It is supposed to be universal for all models that have a picture.
    In case if we have to save an image as a user's profile picture,
    we pass the user as an argument.

    In future, we can add different instance (location, event) as an argument and save the image.

    At the moment it returns an empty dict and 200 status code if picture is uploaded and saved.

    Currently the default format of the image is PNG.
    """
    if request.method != "POST":
        return

    # Upload image image file
    file = request.files["file"]
    assert file
    log(log.INFO, "File uploaded: [%s]", file)

    instance = request.form.get("instance")
    if instance == "event":
        image_type = ImageType.EVENT
        event_unique_id = request.form.get("uniqueId")
        event_query = m.Event.select().where(m.Event.unique_id == event_unique_id)
        event: m.Event = db.session.scalar(event_query)
        if not event:
            log(log.INFO, "Event not found: [%s]", event_unique_id)
            flash("Event not found", "danger")
            return {"error": "Event not found"}, 400

    IMAGE_MAX_WIDTH = app.config["IMAGE_MAX_WIDTH"]
    img = Image.open(file.stream)
    width, height = img.size

    if width > IMAGE_MAX_WIDTH:
        log(log.INFO, "Resizing image")
        ratio = IMAGE_MAX_WIDTH / width
        new_width = IMAGE_MAX_WIDTH
        new_height = int(height * ratio)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img = resized_img

    try:
        img_byte_io = io.BytesIO()
        img.save(img_byte_io, format="PNG")
        img_bytes = img_byte_io.getvalue()
    except Exception as e:
        log(log.ERROR, "Error saving image: [%s]", e)
        flash("Error saving image", "danger")
        return {"error": "Error saving img_bytes"}, 400

    try:
        assert file.filename
        picture = m.Picture(
            filename=file.filename.split("/")[-1],
            file=img_bytes,
        ).save()
        if image_type == ImageType.LOGO:
            user.picture_id = picture.id
            user.save()
            log(log.INFO, "Uploaded image for user: [%s]", user)
            flash("Logo uploaded", "success")
            return {}, 200
        if image_type == ImageType.IDENTIFICATION:
            user.identity_document_id = picture.id
            user.save()
            log(log.INFO, "Uploaded identity document for user: [%s]", user.email)
            return {}, 200
        if image_type == ImageType.EVENT:
            log(log.INFO, "Uploaded image for event: [%s]", event)
            event.picture_id = picture.id
            event.save()
            flash("Event image uploaded", "success")
            return {}, 200
    except Exception as e:
        log(log.ERROR, "Error saving image: [%s]", e)
        flash("Error saving image", "danger")
        return {"error": "Error saving picture"}, 400
