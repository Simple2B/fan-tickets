import filetype
import sqlalchemy as sa

from flask import Blueprint, redirect, url_for, render_template, request, flash
from app import models as m, db, forms as f

from app.logger import log


category_blueprint = Blueprint("category", __name__, url_prefix="/category")


@category_blueprint.route("/")
def category_index():
    return redirect(url_for("admin.category.get_categories"))


@category_blueprint.route("/categories")
def get_categories():
    categories_query = m.Category.select().order_by(m.Category.created_at.asc())
    categories = db.session.scalars(categories_query).all()
    log(log.INFO, "Categories: [%s]", categories)
    return render_template("admin/categories.html", categories=categories)


@category_blueprint.route("/add_category", methods=["GET", "POST"])
def add_category():
    form = f.CategoryForm()

    if request.method == "GET":
        return render_template("admin/category_add.html", form=form)

    if form.validate_on_submit():
        log(log.INFO, "Category form validated: [%s]", form)

        category = db.session.scalar(sa.select(m.Category).where(m.Category.name == form.name.data))
        if category:
            log(log.WARNING, "Category already exists: [%s]", form.name.data)
            flash(f"Category already exists: {form.name.data}", "danger")
            return render_template("admin/category_add.html", form=form)

        category = m.Category(
            name=form.name.data,
        )

        if form.picture.data:
            image_type = filetype.guess(form.picture.data.stream)
            if not image_type.mime.startswith("image"):
                log(log.WARNING, "File is not an image: [%s]", form.picture.data.filename)
                flash(f"Wrong image format: {image_type.mime}", "danger")
                return render_template("admin/category_add.html", form=form)

            category.picture = m.Picture(
                filename=form.picture.data.filename, mimetype=image_type.mime, file=form.picture.data.read()
            )

        db.session.add(category)
        db.session.commit()

        log(log.INFO, "Category saved: [%s]", category)
        flash(f"Category saved: {category.name}", "success")

    elif form.is_submitted():
        log(log.WARNING, "Update category error: [%s]", form.errors)
        flash(f"The given data was invalid. {form.errors}", "danger")

    return redirect(url_for("admin.category.get_categories"))


@category_blueprint.route("/delete_category/<category_id>", methods=["GET"])
def delete_category(category_id):
    category = db.session.get(m.Category, category_id)

    if not category:
        log(log.INFO, "Location not found: [%s]", category_id)
        return redirect(url_for("admin.category.get_categories"))

    if category.picture:
        db.session.delete(category.picture)

    if category.events:
        for event in category.events:
            if event.picture:
                db.session.delete(event.picture)
            if event.tickets:
                for ticket in event.tickets:
                    db.session.delete(ticket)
            db.session.delete(event)

    db.session.delete(category)
    db.session.commit()
    log(log.INFO, "Category deleted: [%s]", category_id)
    return redirect(url_for("admin.category.get_categories"))


@category_blueprint.route("/update_category/<category_id>", methods=["GET", "POST"])
def update_category(category_id: int):
    form = f.CategoryForm()
    category = db.session.get(m.Category, category_id)

    if not category:
        log(log.INFO, "Category not found: [%s]", category_id)
        return redirect(url_for("admin.category.get_categories"))

    if request.method == "GET":
        return render_template("admin/category_update.html", form=form, category=category)

    if form.validate_on_submit():
        category.name = form.name.data
        # update picture
        if form.picture.data:
            image_type = filetype.guess(form.picture.data.stream)
            if not image_type.mime.startswith("image"):
                log(log.WARNING, "File is not an image: [%s]", form.picture.data.filename)
                flash(f"Wrong image format: {image_type.mime}", "danger")
                return render_template("admin/category_update.html", form=form, category=category)

            picture = m.Picture(
                filename=form.picture.data.filename, mimetype=image_type.mime, file=form.picture.data.read()
            )

            if category.picture:
                db.session.delete(category.picture)

            category.picture = picture
        db.session.commit()

    elif form.is_submitted():
        log(log.WARNING, "Update category error: [%s]", form.errors)
        flash(f"The given data was invalid. {form.errors}", "danger")

    return redirect(url_for("admin.category.get_categories"))
