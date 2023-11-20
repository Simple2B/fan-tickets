import io
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app as app,
)
from flask_login import current_user, login_required
from PIL import Image
from app.logger import log
from app import models as m, db


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprint.route("/")
@login_required
def admin():
    users_number = m.User.count()
    locations_number = m.Location.count()
    categories_number = m.Category.count()
    events_number = m.Event.count()
    tickets_number = m.Ticket.count()
    reviews_number = m.Review.count()
    disputes_number = m.Dispute.count()
    notifications_number = m.Notification.count()
    rooms_number = m.Room.count()
    messages_number = m.Message.count()
    return render_template(
        "admin.html",
        users_number=users_number,
        locations_number=locations_number,
        categories_number=categories_number,
        events_number=events_number,
        tickets_number=tickets_number,
        reviews_number=reviews_number,
        disputes_number=disputes_number,
        notifications_number=notifications_number,
        rooms_number=rooms_number,
        messages_number=messages_number,
    )


def image_upload(user):
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
            db.session.add(
                m.Picture(
                    filename=file.filename.split("/")[-1],
                    file=img_byte_arr,
                    mimetype=file.content_type,
                )
            )
            db.session.commit()
            flash("Logo uploaded", "success")
        except Exception as e:
            log(log.ERROR, "Error saving image: [%s]", e)
            flash("Error saving image", "danger")
            return redirect(url_for("main.index"))
        log(log.INFO, "Uploaded image for user: [%s]", user)


@admin_blueprint.route("/picture-upload", methods=["GET", "POST"])
@login_required
def picture_upload():
    query = m.User.select().where(m.User.unique_id == current_user.unique_id)
    user: m.User | None = db.session.scalar(query)

    if not user:
        log(log.INFO, "User not found")
        flash("Incorrect reset password link", "danger")
        return redirect(url_for("main.index"))

    image_upload(user)

    return {"image upload status": "success"}, 200
