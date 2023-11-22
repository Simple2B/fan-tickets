import io
from PIL import Image
from flask import request, flash, current_app as app
from app import models as m
from app.logger import log


def image_upload(user: m.User = None):
    """
    The function for uploading an image to the server.
    It is supposed to be universal for all models that have a picture.
    In case if we have to save an image as a user's profile picture,
    we pass the user as an argument.

    In future, we can add different instance (location, event) as an argument and save the image.

    At the moment it returns an empty dict and 200 status code if picture is uploaded and saved.

    Currently the default format of the image is PNG.
    """
    if request.method == "POST":
        # Upload image image file
        file = request.files["file"]
        log(log.INFO, "File uploaded: [%s]", file)

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
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr = img_byte_arr.getvalue()
        except Exception as e:
            log(log.ERROR, "Error saving image: [%s]", e)
            flash("Error saving image", "danger")
            return {"error": "Error saving img_byte_arr"}, 400

        try:
            picture = m.Picture(
                filename=file.filename.split("/")[-1],
                file=img_byte_arr,
            ).save()
            user.picture_id = picture.id
            user.save()
            log(log.INFO, "Uploaded image for user: [%s]", user)
            flash("Logo uploaded", "success")
            return {}, 200
        except Exception as e:
            log(log.ERROR, "Error saving image: [%s]", e)
            flash("Error saving image", "danger")
            return {"error": "Error saving picture"}, 400
