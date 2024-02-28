from flask import Blueprint, redirect, url_for, render_template, abort
from app import models as m, db, forms as f


settings_blueprint = Blueprint("settings", __name__, url_prefix="/settings")


@settings_blueprint.route("/individual/<user_uuid>", methods=["GET", "POST"])
def individual_settings(user_uuid: str):
    user_query = m.User.select().where(m.User.uuid == user_uuid)
    user: m.User = db.session.scalar(user_query)
    if not user:
        abort(404)
    form = f.IndividualSettingsForm()
    if form.validate_on_submit():
        # form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("admin.users"))
    return render_template("admin/individual_settings.html", form=form, user=user)
