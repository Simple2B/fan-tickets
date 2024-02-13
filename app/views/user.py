from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app import forms as f
from app.database import db
from app import models as m

blueprint_user = Blueprint("users", __name__, url_prefix="/user")


@blueprint_user.route("/profile", methods=["GET"])
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
