from random import randint

import sqlalchemy as sa

from http import HTTPStatus

from flask import Blueprint, render_template, url_for, redirect, flash, request, session, abort
from flask_login import login_user, logout_user, login_required, current_user

from app.controllers.notification_client import NotificationType

from app import models as m
from app import forms as f
from app import schema as s
from app import db
from app import flask_sse_notification, mail_controller
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
            name=form.username.data,
            email=form.email.data,
            picture_id=picture_id,
            password=form.password.data,
            verification_code=verification_code,
        )
        user.save()
        log(log.INFO, "Form submitted. User: [%s]", user)

        mail_controller.send_email(
            (user,),
            "Verify your e-mail",
            render_template(
                "email/email_confirm_web.htm",
                user=user,
            ),
        )

        # send sse notification
        notification_payload = s.NotificationNewUserRegistered(username=user.email)
        flask_sse_notification.notify_admin(
            notification_payload.model_dump(),
            db.session,
            NotificationType.NEW_REGISTRATION,
        )

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
            if user.role == m.UserRole.admin.value:
                return redirect(url_for("admin.user.get_all"))
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
    user_uuid = request.args.get("user_uuid")
    user = db.session.scalar(sa.select(m.User).where(m.User.uuid == user_uuid))

    if not user:
        log(log.INFO, "User not found")
        flash("Activation for this user is failed", "danger")
        return redirect(url_for("main.index"))

    if user.verification_code != verification_code:
        log(log.INFO, "Incorrect verification code")
        flash(
            f"Incorrect email confirmation user-code -{user.verification_code}, verification - {verification_code}",
            "danger",
        )
        return redirect(url_for("main.index"))

    flask_sse_notification.notify_admin(
        s.NotificationUserActivated(email=user.email).model_dump(), db.session, NotificationType.ACCOUNT_VERIFIED
    )

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

    # return render_template("auth/phone.html", reset_password_uuid=reset_password_uuid, form=phone_form)


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
            return redirect(url_for("main.profile"))
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
        user = db.session.scalar(m.User.select().where(m.User.email == form.email.data))

        if not user:
            abort(HTTPStatus.NOT_FOUND)

        user.reset_password()

        # Send reset password link to email
        mail_controller.send_email(
            (user,),
            "Reset password",
            render_template(
                "email/remind.htm",
                user=user,
            ),
        )

        flash(
            "Password reset successful. For set new password please check your e-mail.",
            "success",
        )
    elif form.is_submitted():
        log(log.ERROR, "No registered user with this e-mail")
        flash("No registered user with this e-mail", "danger")
    return render_template("auth/forgot.html", form=form)


@auth_blueprint.route("/password_recovery", methods=["GET", "POST"])
def password_recovery():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    reset_password_uuid = request.args.get("reset_password_uuid")
    email = request.args.get("email")

    if not reset_password_uuid or not email:
        abort(HTTPStatus.BAD_REQUEST)

    user = db.session.scalar(
        sa.select(m.User).where(m.User.reset_password_uuid == reset_password_uuid, m.User.email == email)
    )

    if not user:
        flash("Incorrect reset password link", "danger")
        return redirect(url_for("main.index"))

    form = f.ChangePasswordForm()

    if form.validate_on_submit():
        user.password = form.password.data
        user.save()
        login_user(user)
        flash("Login successful.", "success")
        return redirect(url_for("main.index"))

    user.reset_password()
    return render_template(
        "auth/reset_password.html",
        form=form,
        user=user,
    )
