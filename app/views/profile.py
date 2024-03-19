import io
import csv
from datetime import datetime
from flask import Blueprint, render_template, flash, send_file, url_for, redirect
from flask_login import login_required, current_user
from app import forms as f, models as m
from app.controllers import image_upload, ImageType
from app.logger import log


blueprint_profile = Blueprint("profile", __name__, url_prefix="/profile")


@blueprint_profile.route("/logo-upload", methods=["GET", "POST"])
@login_required
def logo_upload():
    image_upload(
        current_user,
        ImageType.LOGO,
    )
    return {}, 200


@blueprint_profile.route("/edit_email")
@login_required
def edit_email():
    email_form = f.EmailEditForm()
    return render_template(
        "user/email_edit.html",
        user=current_user,
        email_form=email_form,
    )


@blueprint_profile.route("/save_email", methods=["GET", "POST"])
@login_required
def save_email():
    user: m.User = current_user

    email_form = f.EmailEditForm()
    log(log.INFO, "Email change form submitted. User: [%s]", user)
    if email_form.validate_on_submit():
        user.email = email_form.email.data
        user.save()
    else:
        log(log.ERROR, "Email change form errors: [%s]", email_form.errors)
        flash(f"{email_form.errors}", "danger")

    return render_template("user/email_save.html", user=user, email_form=email_form)


@blueprint_profile.route("/edit_phone")
@login_required
def edit_phone():
    phone_form = f.PhoneEditForm()
    return render_template(
        "user/phone_edit.html",
        user=current_user,
        phone_form=phone_form,
    )


@blueprint_profile.route("/save_phone", methods=["GET", "POST"])
@login_required
def save_phone():
    user: m.User = current_user

    phone_form = f.PhoneEditForm()
    if phone_form.validate_on_submit():
        log(log.INFO, "Phone change form submitted. User: [%s]", user)
        user.phone = phone_form.phone.data
        user.save()
    else:
        log(log.ERROR, "Phone change form errors: [%s]", phone_form.errors)
        flash(f"{phone_form.errors}", "danger")

    return render_template("user/phone_save.html", user=user, phone_form=phone_form)


@blueprint_profile.route("/edit_card")
@login_required
def edit_card():
    card_form = f.CardEditForm()
    return render_template(
        "user/card_edit.html",
        user=current_user,
        card_form=card_form,
    )


@blueprint_profile.route("/save_card", methods=["GET", "POST"])
@login_required
def save_card():
    user: m.User = current_user
    CARD_NUMBER_LENGTH = 16

    card_form = f.CardEditForm()
    if card_form.validate_on_submit():
        log(log.INFO, "Card change form submitted. User: [%s]", user)
        user.card = card_form.card.data
        if user.card and len(user.card) == CARD_NUMBER_LENGTH:
            log(log.INFO, "Card activated. User: [%s]", user)
            # TODO: remove after test payment system
            # user.activated = True
        else:
            log(log.INFO, "Card deactivated. User: [%s]", user)
            user.activated = False
        user.save()
    else:
        log(log.ERROR, "Card change form errors: [%s]", card_form.errors)
        flash(f"{card_form.errors}", "danger")

    return render_template("user/card_save.html", user=user, card_form=card_form)


@blueprint_profile.route("/export", methods=["GET", "POST"])
@login_required
def export():
    with io.StringIO() as proxy:
        writer = csv.writer(proxy)
        row = [
            "username",
            "email",
            "phone",
            "card",
        ]
        writer.writerow(row)
        row = [
            current_user.name,
            current_user.email,
            current_user.phone,
            current_user.card,
        ]
        writer.writerow(row)

        # Creating the byteIO object from the StringIO Object
        file_bytes = io.BytesIO()
        file_bytes.write(proxy.getvalue().encode("utf-8"))
        file_bytes.seek(0)

    now = datetime.now()
    return send_file(
        file_bytes,
        as_attachment=True,
        download_name=f"report_{current_user.name}_{now.strftime('%Y-%m-%d-%H-%M-%S')}.csv",
        mimetype="text/csv",
        max_age=0,
        last_modified=now,
    )


@blueprint_profile.route("/deactivate", methods=["GET"])
@login_required
def deactivate():
    user: m.User = current_user
    user.activated = False
    user.save()
    log(log.INFO, "User deactivated. User: [%s]", user)
    flash("User deactivated!", "success")
    return redirect(url_for("auth.login"))
