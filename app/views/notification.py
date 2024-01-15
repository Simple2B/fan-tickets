from flask import render_template, Blueprint
from flask_login import current_user, login_required

from app.database import db


notification_blueprint = Blueprint("notifications", __name__)


@notification_blueprint.route("/")
@login_required
def notifications():
    notifications = db.session.scalars(current_user.notifications.select())

    return render_template("notifications.html", notifications=notifications)
