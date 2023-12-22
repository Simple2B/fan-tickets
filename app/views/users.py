import io
from datetime import datetime
import csv
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    send_file,
)
from flask_login import login_required, current_user
import sqlalchemy as sa
from app.controllers import create_pagination, image_upload, ImageCategory
from app import models as m, db
from app import forms as f
from app.logger import log


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    query = m.User.select().order_by(m.User.id)
    count_query = sa.select(sa.func.count()).select_from(m.User)
    if q:
        query = m.User.select().where(m.User.username.like(f"{q}%") | m.User.email.like(f"{q}%")).order_by(m.User.id)
        count_query = (
            sa.select(sa.func.count())
            .where(m.User.username.like(f"{q}%") | m.User.email.like(f"{q}%"))
            .select_from(m.User)
        )

    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "user/users.html",
        users=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/save", methods=["POST"])
@login_required
def save():
    form = f.UserForm()
    if form.validate_on_submit():
        query = m.User.select().where(m.User.id == int(form.user_id.data))
        u: m.User | None = db.session.scalar(query)
        if not u:
            log(log.ERROR, "Not found user by id : [%s]", form.user_id.data)
            flash("Cannot save user data", "danger")
        else:
            u.username = form.username.data
            u.email = form.email.data
            u.activated = form.activated.data
            if form.password.data.strip("*\n "):
                u.password = form.password.data
            u.save()
        if form.next_url.data:
            return redirect(form.next_url.data)
        return redirect(url_for("user.get_all"))

    else:
        log(log.ERROR, "User save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("user.get_all"))


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.NewUserForm()
    if form.validate_on_submit():
        user = m.User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
        )
        log(log.INFO, "Form submitted. User: [%s]", user)
        flash("User added!", "success")
        user.save()
        return redirect(url_for("user.get_all"))


# TODO: create admins and clients separately (by admin only)


@bp.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete(id: int):
    user_query = m.User.select().where(m.User.id == id)
    user: m.User = db.session.scalar(user_query)
    if not user:
        log(log.INFO, "There is no user with id: [%s]", id)
        flash("There is no such user", "danger")
        return "no user", 404

    user.activated = False
    user.save()
    log(log.INFO, "User deleted. User: [%s]", user)
    flash("User deleted!", "success")
    return "ok", 200


@bp.route("/deactivate", methods=["GET"])
@login_required
def deactivate():
    user: m.User = current_user
    user.activated = False
    user.save()
    log(log.INFO, "User deactivated. User: [%s]", user)
    flash("User deactivated!", "success")
    return redirect(url_for("auth.login"))


@bp.route("/profile", methods=["GET"])
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


@bp.route("/logo-upload", methods=["GET", "POST"])
@login_required
def logo_upload():
    image_upload(
        current_user,
        ImageCategory.LOGO,
    )
    return {}, 200


@bp.route("/edit_email")
@login_required
def edit_email():
    email_form = f.EmailEditForm()
    return render_template(
        "user/email_edit.html",
        user=current_user,
        email_form=email_form,
    )


@bp.route("/save_email", methods=["GET", "POST"])
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


@bp.route("/edit_phone")
@login_required
def edit_phone():
    phone_form = f.PhoneEditForm()
    return render_template(
        "user/phone_edit.html",
        user=current_user,
        phone_form=phone_form,
    )


@bp.route("/save_phone", methods=["GET", "POST"])
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


@bp.route("/edit_card")
@login_required
def edit_card():
    card_form = f.CardEditForm()
    return render_template(
        "user/card_edit.html",
        user=current_user,
        card_form=card_form,
    )


@bp.route("/save_card", methods=["GET", "POST"])
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
            user.activated = True
        else:
            log(log.INFO, "Card deactivated. User: [%s]", user)
            user.activated = False
        user.save()
    else:
        log(log.ERROR, "Card change form errors: [%s]", card_form.errors)
        flash(f"{card_form.errors}", "danger")

    return render_template("user/card_save.html", user=user, card_form=card_form)


@bp.route("/set_notifications", methods=["GET", "POST"])
@login_required
def set_notifications():
    form = f.NotificationsConfigForm()
    if form.validate_on_submit():
        user: m.User = current_user
        user.notifications_config.new_event = form.new_event.data
        user.notifications_config.new_ticket = form.new_ticket.data
        user.notifications_config.new_message = form.new_message.data
        user.notifications_config.new_buyers_payment = form.new_buyers_payment.data
        user.notifications_config.your_payment_received = form.your_payment_received.data
        user.notifications_config.ticket_transfer_confirmed = form.ticket_transfer_confirmed.data
        user.notifications_config.dispute_started = form.dispute_started.data
        user.notifications_config.dispute_resolved = form.dispute_resolved.data
        user.save()
        log(log.INFO, "Notifications settings saved. User: [%s]", user)
        flash("Notifications settings saved!", "success")
    else:
        log(log.ERROR, "Notifications settings save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
    return render_template("user/notifications_save.html", user=user)


@bp.route("/export", methods=["GET", "POST"])
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
