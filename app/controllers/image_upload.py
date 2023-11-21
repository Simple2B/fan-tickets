import io
from PIL import Image
from flask import request, redirect, url_for, flash, current_app as app
from app import models as m
from app.logger import log


def image_upload(user: m.User):
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
            return redirect(url_for("auth.image_upload", user_unique_id=user.unique_id))

        try:
            picture = m.Picture(
                filename=file.filename.split("/")[-1],
                file=img_byte_arr,
                mimetype=file.content_type,
            ).save()
            user.picture_id = picture.id
            user.save()
            flash("Logo uploaded", "success")
        except Exception as e:
            log(log.ERROR, "Error saving image: [%s]", e)
            flash("Error saving image", "danger")
            return redirect(url_for("main.index"))
        log(log.INFO, "Uploaded image for user: [%s]", user)
