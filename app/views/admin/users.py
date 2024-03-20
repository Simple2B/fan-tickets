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
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination
from app import models as m, db
from app import forms as f
from app.logger import log


blueprint_user = Blueprint("user", __name__, url_prefix="/user")


@blueprint_user.route("/users", methods=["GET"])
@login_required
def get_all():
    search = request.args.get("search")
    q = request.args.get("q")
    pg = request.args.get("pg")
    query = m.User.select().where(m.User.activated.is_(True)).order_by(m.User.id)
    count_query = sa.select(sa.func.count()).select_from(m.User).where(m.User.activated.is_(True))

    template = "user/users.html"

    if q or search:
        query = query.where(m.User.username.ilike(f"%{q}%") | m.User.email.ilike(f"%{q}%")).order_by(m.User.id)
        count_query = count_query.where(m.User.username.ilike(f"%{q}%") | m.User.email.ilike(f"%{q}%")).select_from(
            m.User
        )
        if pg:
            template = "user/users.html"
        else:
            template = "user/search.html"

    # Download
    if request.args.get("download"):
        log(log.INFO, "Downloading users table")
        users = db.session.scalars(query).all()
        with io.StringIO() as proxy:
            writer = csv.writer(proxy)
            row = [
                "#",
                "First Name",
                "Last Name",
                "Email",
                "Phone",
                "Address",
                "Is activated",
            ]
            writer.writerow(row)
            for index, user in enumerate(users):
                row = [
                    str(index),
                    user.name,
                    user.last_name,
                    user.email,
                    user.phone,
                    user.address,
                    user.activated,
                ]
                writer.writerow(row)

            mem = io.BytesIO()
            mem.write(proxy.getvalue().encode("utf-8"))
            mem.seek(0)

        now = datetime.now()

        return send_file(
            mem,
            as_attachment=True,
            download_name=f"fan_ticket_users_{now.strftime('%Y-%m-%d-%H-%M-%S')}.csv",
            mimetype="text/csv",
            max_age=0,
            last_modified=now,
        )

    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        template,
        users=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@blueprint_user.route("/save", methods=["POST"])
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
        return redirect(url_for("admin.user.get_all"))

    else:
        log(log.ERROR, "User save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("admin.user.get_all"))


@blueprint_user.route("/delete/<int:id>", methods=["DELETE"])
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
