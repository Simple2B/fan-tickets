import filetype
import sqlalchemy as sa

from flask import Blueprint, redirect, url_for, render_template, request, flash
from app import models as m, db, forms as f
from app.logger import log


location_blueprint = Blueprint("location", __name__, url_prefix="/location")


@location_blueprint.route("/")
def location_index():
    return redirect(url_for("location.get_locations"))


@location_blueprint.route("/locations")
def get_locations():
    locations = db.session.scalars(sa.select(m.Location).where(m.Location.deleted.is_(False)).order_by(m.Location.name))
    log(log.INFO, "Locations: [%s]", locations)
    return render_template("admin/locations.html", locations=locations)


@location_blueprint.route("/add_location", methods=["GET", "POST"])
def add_location():
    form = f.LocationForm()
    if request.method == "GET":
        return render_template("admin/location_add.html", form=form)

    if form.validate_on_submit():
        log(log.INFO, "Location form validated: [%s]", form)

        location = db.session.scalar(sa.select(m.Location).where(m.Location.name == form.name.data))
        if location:
            log(log.WARNING, "Location already exists: [%s]", form.name.data)
            flash(f"Location already exists: {form.name.data}", "danger")
            return render_template("admin/location_add.html", form=form)

        location = m.Location(
            name=form.name.data,
        )

        if form.picture.data:
            image_type = filetype.guess(form.picture.data.stream)
            if not image_type.mime.startswith("image"):
                log(log.WARNING, "File is not an image: [%s]", form.picture.data.filename)
                flash(f"Wrong image format: {image_type.mime}", "danger")
                return render_template("admin/location_add.html", form=form)

            location.picture = m.Picture(
                filename=form.picture.data.filename, mimetype=image_type.mime, file=form.picture.data.read()
            )

        db.session.add(location)
        db.session.commit()

        log(log.INFO, "Location saved: [%s]", location)
        return redirect(url_for("admin.location.get_locations"))

    else:
        log(log.INFO, "Location form not validated: [%s]", form.errors)
        return render_template("admin/location_add.html", form=form)


@location_blueprint.route("/location_delete/<location_id>", methods=["GET"])
def location_delete(location_id):
    location = db.session.get(m.Location, location_id)

    if not location:
        log(log.INFO, "Location not found: [%s]", location_id)
        return redirect(url_for("admin.location.get_locations"))

    location.deleted = True
    db.session.commit()
    log(log.INFO, "Location deleted: [%s]", location_id)
    return redirect(url_for("admin.location.get_locations"))


@location_blueprint.route("/update_location/<location_id>", methods=["GET", "POST"])
def update_location(location_id: int):
    form = f.LocationForm()
    location = db.session.get(m.Location, location_id)

    if not location:
        log(log.INFO, "Category not found: [%s]", location_id)
        return redirect(url_for("admin.location.get_locations"))

    if request.method == "GET":
        return render_template("admin/location_update.html", form=form, location=location)

    if form.validate_on_submit():
        location.name = form.name.data
        # update picture
        if form.picture.data:
            image_type = filetype.guess(form.picture.data.stream)
            if not image_type.mime.startswith("image"):
                log(log.WARNING, "File is not an image: [%s]", form.picture.data.filename)
                flash(f"Wrong image format: {image_type.mime}", "danger")
                return render_template("admin/location_update.html", form=form, location=location)

            picture = m.Picture(
                filename=form.picture.data.filename, mimetype=image_type.mime, file=form.picture.data.read()
            )

            if location.picture and not db.session.scalar(
                sa.select(m.Location).where(m.Location.id != location.id, m.Location.picture_id == location.picture.id)
            ):
                db.session.delete(location.picture)

            location.picture = picture
        db.session.commit()

    elif form.is_submitted():
        log(log.WARNING, "Update category error: [%s]", form.errors)
        flash(f"The given data was invalid. {form.errors}", "danger")

    return redirect(url_for("admin.location.get_locations"))
