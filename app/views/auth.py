import os
from random import randint
from flask_mail import Message
from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask import current_app as app
from flask_login import login_user, logout_user, login_required, current_user

from app import models as m
from app import forms as f
from app import mail, db
from app.logger import log


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = f.RegistrationForm()
    if form.validate_on_submit():
        picture_query = m.Picture.select().where(m.Picture.filename.ilike(f"%{'default_avatar'}%"))
        picture: m.Picture = db.session.scalar(picture_query)
        picture_id = picture.id if picture else None
        verification_code = randint(100000, 999999)
        user = m.User(
            username=form.username.data,
            email=form.email.data,
            picture_id=picture_id,
            password=form.password.data,
            verification_code=verification_code,
        )
        user.save()
        log(log.INFO, "Form submitted. User: [%s]", user)

        # create e-mail message
        msg = Message(
            subject="Verify your e-mail",
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email],
        )
        # TODO: add production url
        if os.environ.get("APP_ENV") == "development":
            url = url_for(
                "auth.activate",
                user_id=user.unique_id,
                verification_code=verification_code,
                _external=True,
            )
        else:
            base_url = app.config["STAGING_BASE_URL"]
            url = f"{base_url}activated?user_id={user.unique_id}&verification_code={verification_code}"

        msg.html = render_template(
            "email/email_confirm_web.htm",
            user=user,
            url=url,
        )
        mail.send(msg)

        flash("Registration successful. Checkout you email for confirmation!", "success")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        log(log.WARNING, "Form submitted error: [%s]", form.errors)
        flash(f"The given data was invalid. {form.errors}", "danger")

    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("events.get_events"))
    form = f.LoginForm(request.form)
    if form.validate_on_submit():
        user = m.User.authenticate(form.user_id.data, form.password.data)
        log(log.INFO, "Form submitted. User: [%s]", user)
        if user:
            login_user(user)
            log(log.INFO, "Login successful.")
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
        flash("Wrong user ID or password.", "danger")

    elif form.is_submitted():
        log(log.WARNING, "Form submitted error: [%s]", form.errors)
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    log(log.INFO, "You were logged out.")
    session.clear()
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/activated", methods=["GET", "POST"])
def activate():
    verification_code = request.args.get("verification_code")
    user_id = request.args.get("user_id")
    query = m.User.select().where(m.User.unique_id == user_id)
    user: m.User | None = db.session.scalar(query)

    if not user:
        log(log.INFO, "User not found")
        flash("Incorrect email confirmation", "danger")
        return redirect(url_for("main.index"))

    if user.verification_code != verification_code:
        log(log.INFO, "Incorrect verification code")
        flash("Incorrect email confirmation", "danger")
        return redirect(url_for("main.index"))

    # TODO: remove after testing registration flow
    # user.activated = True
    user.save()
    login_user(user)
    log(log.INFO, "User activated")
    flash("Email confirmed", "success")
    return redirect(url_for("main.index"))

    # TODO: phone verification will be added later
    # if phone_form.validate_on_submit():
    # twilio credentials
    # account_sid = app.config["TWILIO_ACCOUNT_SID"]
    # auth_token = app.config["TWILIO_AUTH_TOKEN"]
    # sender = app.config["TWILIO_PHONE_NUMBER"]
    # receiver = phone_form.phone.data
    # client = Client(account_sid, auth_token)

    # verification via twilio
    # verification_code = randint(100000, 999999)
    # message = client.messages.create(from_=sender, body=verification_code, to=receive

    # TODO: hardcoded verification code while twilio is not working
    # verification_code = "123456"

    #     user.verification_code = str(verification_code)
    #     user.phone = phone_form.phone.data
    #     user.save()
    #     login_user(user)

    #     log(log.INFO, "Form submitted. Message: [%s]", verification_code)
    #     flash("Um código de confirmação foi enviado para o seu telefone.", "success")
    #     return redirect(url_for("auth.phone_verification"))

    # return render_template("auth/phone.html", reset_password_uid=reset_password_uid, form=phone_form)


@auth_blueprint.route("/phone_verification", methods=["GET", "POST"])
@login_required
def phone_verification():
    form = f.VerificationCodeForm()

    if request.method == "GET":
        log(log.INFO, "Render phone verification page without blank form")
        return render_template("auth/phone_verification.html", form=form)

    if form.validate_on_submit():
        full_code = f"{form.digit_1.data}{form.digit_2.data}{form.digit_3.data}{form.digit_4.data}{form.digit_5.data}{form.digit_6.data}"
        user = db.session.get(m.User, current_user.id)
        log(log.INFO, "Verification code: [%s], User: [%s]", full_code, user)
        if user.verification_code == full_code:
            log(log.INFO, "Verification code is correct: [%s]", full_code)
            flash("Código de verificação correto.", "success")
            return redirect(url_for("user.profile"))
        else:
            log(log.INFO, "Verification code is incorrect: [%s]", full_code)
            flash("Código de verificação inválido!", "danger")
    else:
        log(log.INFO, "Verification code is incorrect: [%s]", form.errors)
        flash("Código de verificação inválido!", "danger")

    return render_template("auth/phone_verification.html", form=form)


@auth_blueprint.route("/forgot", methods=["GET", "POST"])
def forgot_pass():
    form = f.ForgotForm(request.form)
    if form.validate_on_submit():
        query = m.User.select().where(m.User.email == form.email.data)
        user: m.User = db.session.scalar(query)
        # create e-mail message
        msg = Message(
            subject="Reset password",
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email],
        )
        url = url_for(
            "auth.password_recovery",
            reset_password_uid=user.unique_id,
            _external=True,
        )
        msg.html = render_template(
            "email/remind.htm",
            user=user,
            url=url,
        )
        mail.send(msg)
        user.reset_password()
        flash(
            "Password reset successful. For set new password please check your e-mail.",
            "success",
        )
    elif form.is_submitted():
        log(log.ERROR, "No registered user with this e-mail")
        flash("No registered user with this e-mail", "danger")
    return render_template("auth/forgot.html", form=form)


@auth_blueprint.route("/password_recovery/<reset_password_uid>", methods=["GET", "POST"])
def password_recovery(reset_password_uid):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    query = m.User.select().where(m.User.unique_id == reset_password_uid)
    user: m.User = db.session.scalar(query)

    if not user:
        flash("Incorrect reset password link", "danger")
        return redirect(url_for("main.index"))

    form = f.ChangePasswordForm()

    if form.validate_on_submit():
        user.password = form.password.data
        user.activated = True
        user.unique_id = m.gen_password_reset_id()
        user.save()
        login_user(user)
        flash("Login successful.", "success")
        return redirect(url_for("main.index"))

    return render_template(
        "auth-admin/reset_password.html",
        form=form,
        unique_id=reset_password_uid,
    )
