from flask import (
    Blueprint,
    render_template,
)
from flask_login import current_user, login_required
from app import models as m
from app.controllers.image_upload import image_upload, ImageType


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


@admin_blueprint.route("/picture-upload", methods=["GET", "POST"])
@login_required
def picture_upload():
    user: m.User = current_user
    image_upload(user, ImageType.LOGO)
    return {}, 200
