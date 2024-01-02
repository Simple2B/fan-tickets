from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_required
from app import models as m
from app.controllers.image_upload import image_upload, ImageType


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprint.route("/")
@login_required
def admin():
    return redirect(url_for("user.get_all"))


@admin_blueprint.route("/picture-upload", methods=["GET", "POST"])
@login_required
def picture_upload():
    user: m.User = current_user
    image_upload(user, ImageType.LOGO)
    return {}, 200
