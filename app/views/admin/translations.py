import re
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
        text_en = re.sub(r"\s+", " ", form.en.data)
        translation_query = sa.select(m.Translation).where(m.Translation.en == text_en)
        translation: m.Translation = db.session.scalar(translation_query)

        if translation:
            log(log.WARNING, "Translation already exists: [%s]", text_en)
            flash(f"Translation already exists: {text_en}", "danger")
            return render_template("admin/add_translation.html", form=form)

        translation = m.Translation(
            name=form.name.data,
            en=text_en,
            pt=form.pt.data,
        ).save()

        log(log.INFO, "Translation saved: [%s]", translation)
        return redirect(url_for("admin.translations.get_all"))


@translations_blueprint.route("/update/<translation_id>", methods=["GET", "POST"])
def update(translation_id: int):
    form = f.TranslationForm()

    translation = db.session.get(m.Translation, translation_id)

    if not translation:
        log(log.WARNING, "Translation not found: [%s]", translation_id)
        flash("Translation not found", "danger")
        return redirect(url_for("admin.translations.get_all"))

    if request.method == "GET":
        return render_template("admin/translation_update.html", form=form, translation=translation)

    if form.validate_on_submit():
        text_en = re.sub(r"\s+", " ", form.en.data)
        translation.name = form.name.data
        translation.en = text_en
        translation.pt = form.pt.data

        db.session.commit()

        log(log.INFO, "Translation updated: [%s]", translation)
        return redirect(url_for("admin.translations.get_all"))


@translations_blueprint.route("/delete/<translation_id>", methods=["GET"])
def delete(translation_id):
    translation = db.session.get(m.Translation, translation_id)

    if not translation:
        log(log.WARNING, "Translation not found: [%s]", translation_id)
        flash("Translation not found", "danger")
        return redirect(url_for("admin.translations.get_all"))

    db.session.delete(translation)
    db.session.commit()
    log(log.INFO, "Translation deleted: [%s]", translation_id)

    flash("Translation deleted", "success")
    return redirect(url_for("admin.translations.get_all"))
