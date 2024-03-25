from sqlalchemy.exc import IntegrityError

from flask import request, Blueprint, render_template, redirect, url_for, current_app as app
from flask_login import login_user

from app import controllers as c
from app import schema as s
from app import models as m, db
from app.logger import log
from config import config

CFG = config()

user_social_profile_blueprint = Blueprint("user_social_profile", __name__, url_prefix="/user_social_profile")


@user_social_profile_blueprint.route("/create", methods=["GET", "POST"])
def create():
    try:
        params = s.ChatAuthSocialProfileParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if params.without_social_profile:
        login_user(user)
        c.save_message(
            "You have successfully registered. The history will be emailed and deleted after selecting an action",
            "Without social profile",
            room,
        )

        log(log.INFO, f"User: {user.email} logged in")

        if room.ticket:
            return redirect(
                url_for(
                    "buy.booking_ticket",
                    room_unique_id=room.unique_id,
                    user_unique_id=user.uuid,
                    ticket_unique_id=room.ticket.unique_id,
                )
            )
        return render_template(
            "chat/registration/verified.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    if params.facebook:
        c.create_social_profile(params, user, room)
        try:
            db.session.commit()
            log(log.INFO, "Facebook added: [%s]", params.user_message)

            return render_template(
                "chat/registration/profile_instagram.html",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )
        except IntegrityError as e:
            db.session.rollback()
            log(log.ERROR, "Facebook is not added: [%s]", e)
            return render_template(
                "chat/registration/profile_facebook.html",
                error_message="Form submitting error. Please add your facebook url again",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )

    if params.without_facebook:
        c.save_message("Do you want to add your facebook profile?", "Without facebook profile", room)
        log(log.INFO, "Without facebook")

        return render_template(
            "chat/registration/profile_instagram.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    if params.instagram:
        c.create_social_profile(params, user, room)
        try:
            db.session.commit()
            log(log.INFO, "Instagram added: [%s]", params.user_message)

            return render_template(
                "chat/registration/profile_twitter.html",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )
        except IntegrityError as e:
            db.session.rollback()
            log(log.ERROR, "Instagram is not added: [%s]", e)
            return render_template(
                "chat/registration/profile_instagram.html",
                error_message="Form submitting error. Please add your instagram url again",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )

    if params.without_instagram:
        c.save_message("Do you want to add your instagram profile?", "Without instagram profile", room)
        log(log.INFO, "Without instagram")

        return render_template(
            "chat/registration/profile_twitter.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    if params.twitter:
        c.create_social_profile(params, user, room)
        try:
            db.session.commit()
            log(log.INFO, "Twitter added: [%s]", params.user_message)

            login_user(user)
            m.Message(
                sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
                room_id=room.id,
                text="You have successfully registered",
            ).save()
            log(log.INFO, f"User: {user.email} logged in")

            if room.ticket:
                return redirect(
                    url_for(
                        "buy.booking_ticket",
                        room_unique_id=room.unique_id,
                        user_unique_id=user.uuid,
                        ticket_unique_id=room.ticket.unique_id,
                    )
                )

            return render_template(
                "chat/registration/verified.html",
                room=room,
                now=c.utcnow_chat_format(),
            )
        except IntegrityError as e:
            db.session.rollback()
            log(log.ERROR, "Twitter is not added: [%s]", e)
            return render_template(
                "chat/registration/profile_twitter.html",
                error_message="Form submitting error. Please add your twitter url again",
                room=room,
                now=c.utcnow_chat_format(),
                user_unique_id=params.user_unique_id,
            )

    if params.without_twitter:
        c.save_message("Do you want to add your twitter profile?", "Without twitter profile", room)
        log(log.INFO, "Without twitter")
        login_user(user)
        m.Message(
            sender_id=app.config["CHAT_DEFAULT_BOT_ID"],
            room_id=room.id,
            text="You have successfully registered",
        ).save()
        log(log.INFO, f"User: {user.email} logged in")

        if room.ticket:
            return redirect(
                url_for(
                    "buy.booking_ticket",
                    room_unique_id=room.unique_id,
                    user_unique_id=user.uuid,
                    ticket_unique_id=room.ticket.unique_id,
                )
            )
        return render_template(
            "chat/registration/verified.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.facebook and not params.instagram and not params.twitter:
        log(log.ERROR, "No social profiles: [%s]", params.facebook)
        return render_template(
            "chat/registration/profile_facebook.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    if room.ticket:
        return redirect(
            url_for(
                "buy.booking_ticket",
                room_unique_id=room.unique_id,
                user_unique_id=user.uuid,
                ticket_unique_id=room.ticket.unique_id,
            )
        )

    return render_template(
        "chat/registration/verified.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=params.user_unique_id,
    )
