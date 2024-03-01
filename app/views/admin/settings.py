from flask import Blueprint, request, redirect, url_for, render_template, flash, abort
from app import models as m, db, forms as f
from app.logger import log


settings_blueprint = Blueprint("settings", __name__, url_prefix="/settings")


@settings_blueprint.route("/individual/<user_uuid>", methods=["GET", "POST"])
def individual(user_uuid: str):
    user_query = m.User.select().where(m.User.uuid == user_uuid)
    user: m.User = db.session.scalar(user_query)
    if not user:
        abort(404)

    form = f.FeeSettingsForm()

    if request.method == "GET":
        form.service_fee.data = user.service_fee
        form.bank_fee.data = user.bank_fee
        log(
            log.INFO,
            f"{user.name} {user.last_name} service_fee: {form.service_fee.data}, bank_fee: {form.bank_fee.data}",
        )
        return render_template("admin/individual_settings.html", form=form, user=user)

    if form.validate_on_submit():
        user.service_fee = form.service_fee.data
        user.bank_fee = form.bank_fee.data
        user.save()
        log(log.INFO, f"User {user.name} {user.last_name} fee settings updated")
        flash(f"User {user.name} {user.last_name} fee settings updated")
        return redirect(url_for("admin.settings.individual", user_uuid=user_uuid))
    else:
        log(log.ERROR, "Form validation failed [%s], [%s]", form.errors, form.data)
        return render_template("admin/global_settings.html", form=form)


@settings_blueprint.route("/general", methods=["GET", "POST"])
def general():
    global_fee_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())

    if not global_fee_settings:
        log(log.ERROR, "Global fee settings not found")
        global_fee_settings = m.GlobalFeeSettings(
            service_fee=5,
            bank_fee=6,
        ).save()
        log(log.INFO, "Global fee settings created")

    form = f.FeeSettingsForm(sorting_type=global_fee_settings.tickets_sorting_by)
    if request.method == "GET":
        form.service_fee.data = global_fee_settings.service_fee
        form.bank_fee.data = global_fee_settings.bank_fee
        # form.selling_limit.data = global_fee_settings.selling_limit
        # form.buying_limit.data = global_fee_settings.buying_limit
        log(
            log.INFO,
            f"General service_fee: {form.service_fee.data}, bank_fee: {form.bank_fee.data}",
        )
        return render_template("admin/global_settings.html", form=form)

    if form.validate_on_submit():
        global_fee_settings.service_fee = form.service_fee.data
        global_fee_settings.bank_fee = form.bank_fee.data
        global_fee_settings.tickets_sorting_by = form.tickets_sorting_by.data
        global_fee_settings.save()
        log(log.INFO, "Global fee settings updated")
        flash("Global fee settings updated")
        return redirect(url_for("admin.settings.general"))
    else:
        log(log.ERROR, "Form validation failed [%s], [%s]", form.errors, form.data)
        return render_template("admin/global_settings.html", form=form)
