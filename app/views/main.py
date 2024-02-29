from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app import models as m, db, forms as f


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


@main_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    user: m.User = current_user
    payments_query = m.Payment.select().where(m.Payment.buyer_id == user.id)
    payments = db.session.scalars(payments_query).all()

    email_form = f.EmailEditForm()
    phone_form = f.PhoneEditForm()
    card_form = f.CardEditForm()
    return render_template(
        "user/profile.html",
        user=user,
        payments=payments,
        email_form=email_form,
        phone_form=phone_form,
        card_form=card_form,
    )
