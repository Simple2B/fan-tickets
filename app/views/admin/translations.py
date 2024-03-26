from flask import Blueprint, request, redirect, url_for, render_template, flash, abort
import sqlalchemy as sa
from app import models as m, db, forms as f
from app.logger import log


translations_blueprint = Blueprint("translations", __name__, url_prefix="/translations")


@translations_blueprint.route("/")
def get_all():
    translations_query = m.Translation.select()
    translations: m.Translation = db.session.scalars(translations_query).all()

    return render_template("admin/translations.html", translations=translations)


@translations_blueprint.route("/add", methods=["GET", "POST"])
def add():
    form = f.TranslationForm()

    if request.method == "GET":
        return render_template("admin/add_translation.html", form=form)

    if form.validate_on_submit():
        translation_query = sa.select(m.Translation).where(m.Translation.en == form.en.data)
        translation: m.Translation = db.session.scalar(translation_query)

        if translation:
            log(log.WARNING, "Translation already exists: [%s]", form.en.data)
            flash(f"Translation already exists: {form.en.data}", "danger")
            return render_template("admin/add_translation.html", form=form)

        translation = m.Translation(
            name=form.name.data,
            en=form.en.data,
            pt=form.pt.data,
        ).save()

        log(log.INFO, "Translation saved: [%s]", translation)
        return redirect(url_for("admin.translations.get_all"))
