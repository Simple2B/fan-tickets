from flask import render_template, Blueprint
from app import models as m, db


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    events = db.session.scalars(m.Event.select().limit(8)).all()
    locations = db.session.scalars(m.Location.select()).all()
    return render_template(
        "landing/home/index.html",
        events=events,
        locations=locations,
    )


@main_blueprint.route("/help")
def help():
    return render_template("help.html")
