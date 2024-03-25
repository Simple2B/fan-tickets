from datetime import datetime
from sqlalchemy import or_


from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user

from app import controllers as c
from app import schema as s
from app import models as m, db
from app.logger import log
from app import mail_controller
from app.controllers.jinja_globals import transactions_last_month
from config import config

CFG = config()

chat_blueprint = Blueprint("chat", __name__, url_prefix="/chat")


@chat_blueprint.route("/open", methods=["GET"])
def open():
    return render_template(
        "chat/chat_home.html",
        now=c.utcnow_chat_format(),
    )


@chat_blueprint.route("/close", methods=["GET"])
def close():
    room_unique_id = request.args.get("room_unique_id")
    if not room_unique_id:
        return render_template(
            "chat/chat_close.html",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    messages_query = m.Message.select().where(m.Message.room_id == room.id)
    messages = db.session.scalars(messages_query).all()

    if current_user.is_authenticated:
        mail_controller.send_email(
            (current_user,),
            f"Today's chat history {datetime.now().strftime(app.config['DATE_CHAT_HISTORY_FORMAT'])}",
            render_template(
                "email/chat_history.htm",
                user=current_user,
                messages=messages,
            ),
        )

    for message in messages:
        db.session.delete(message)
    db.session.commit()

    return render_template(
        "chat/chat_bot_close.html",
        now=c.utcnow_chat_format(),
        room=room,
    )


@chat_blueprint.route("/sell", methods=["GET", "POST"])
def sell():
    seller_id = current_user.id if current_user.is_authenticated else None
    room_unique_id = request.args.get("room_unique_id")
    renew_search = request.args.get("renew_search")
    save_history = request.args.get("save_history", False, type=bool)
    room = None
    template = "chat/chat_auth.html"

    if save_history:
        if not room_unique_id:
            log(log.ERROR, "room_unique_id is not provided")
            return render_template(
                "chat/chat_error.html",
                error_message="Form submitting error",
                now=c.utcnow_chat_format(),
            )
        room = c.get_room(room_unique_id)

        if not room:
            log(log.ERROR, "Room not found: [%s]", room_unique_id)
            return render_template(
                "chat/chat_error.html",
                error_message="Form submitting error",
                now=c.utcnow_chat_format(),
            )

        messages_query = m.Message.select().where(m.Message.room_id == room.id)
        messages = db.session.scalars(messages_query).all()

        if current_user.is_authenticated:
            mail_controller.send_email(
                (current_user,),
                f"Today's chat history {datetime.now().strftime(app.config['DATE_CHAT_HISTORY_FORMAT'])}",
                render_template(
                    "email/chat_history.htm",
                    user=current_user,
                    messages=messages,
                ),
            )

        for message in messages:
            db.session.delete(message)
        db.session.commit()

    if room_unique_id:
        room = c.get_room(room_unique_id)
        c.save_message(
            f"{current_user.name}, how can I assist you? Are you looking to buy or sell a ticket?",
            "Sell",
            room,
        )
    elif current_user.is_authenticated and (current_user.seller_chat_rooms or current_user.buyer_chat_rooms):
        rooms_query = (
            m.Room.select()
            .where(
                or_(m.Room.seller_id == current_user.id, m.Room.buyer_id == current_user.id),
                m.Room.type_of != m.RoomType.DISPUTE.value,
            )
            .order_by(m.Room.id.desc())
        )
        room = db.session.scalar(rooms_query)
    else:
        room = m.Room(
            seller_id=seller_id,
            buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
        ).save()
        assert room
        c.save_message(
            "Hello! Welcome to FanTicketBot. How can I assist you today? Are you looking to buy or sell a ticket?",
            "Sell",
            room,
        )
    assert room
    if renew_search:
        c.save_message("Choose action", "Renew search", room)
        log(log.ERROR, "Renew search")

    categories = []
    if current_user.is_authenticated and current_user.activated:
        template = "chat/sell/event_category.html"
        categories_query = m.Category.select().where(m.Category.deleted.is_(False))
        categories = db.session.scalars(categories_query).all()
    elif not current_user.is_authenticated:
        template = "chat/chat_auth.html"
    elif not current_user.activated and not current_user.identity_document:
        return render_template(
            "chat/registration/passport_identity_number.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=current_user.uuid,
        )
    elif not current_user.activated and not current_user.name:
        return render_template(
            "chat/registration/name.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=current_user.uuid,
        )
    elif not current_user.activated and not current_user.last_name:
        return render_template(
            "chat/registration/last_name.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=current_user.uuid,
        )
    elif not current_user.activated and not current_user.phone:
        return render_template(
            "chat/registration/phone.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=current_user.uuid,
        )
    elif not current_user.activated and not current_user.address:
        return render_template(
            "chat/registration/address.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=current_user.uuid,
        )
    elif not current_user.activated and not current_user.birth_date:
        return render_template(
            "chat/registration/birth_date.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=current_user.uuid,
        )

    if current_user.is_authenticated:
        global_fee_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
        if transactions_last_month(current_user) > global_fee_settings.selling_limit:
            return render_template(
                "chat/buy/transactions_limit.html",
                error_message="You have reached the limit of transactions per month",
                now=c.utcnow_chat_format(),
                room=room,
            )

    return render_template(
        template,
        locations=m.Location.all(),
        categories=categories,
        now=c.utcnow_chat_format(),
        room=room,
    )


@chat_blueprint.route("/buy")
def buy():
    room_unique_id = request.args.get("room_unique_id")
    save_history = request.args.get("save_history", False, type=bool)

    if save_history:
        if not room_unique_id:
            log(log.ERROR, "room_unique_id is not provided")
            return render_template(
                "chat/chat_error.html",
                error_message="Form submitting error",
                now=c.utcnow_chat_format(),
            )
        room = c.get_room(room_unique_id)

        if not room:
            log(log.ERROR, "Room not found: [%s]", room_unique_id)
            return render_template(
                "chat/chat_error.html",
                error_message="Form submitting error",
                now=c.utcnow_chat_format(),
            )

        messages_query = m.Message.select().where(m.Message.room_id == room.id)
        messages = db.session.scalars(messages_query).all()

        if current_user.is_authenticated:
            mail_controller.send_email(
                (current_user,),
                f"Today's chat history {datetime.now().strftime(app.config['DATE_CHAT_HISTORY_FORMAT'])}",
                render_template(
                    "email/chat_history.htm",
                    user=current_user,
                    messages=messages,
                ),
            )

        for message in messages:
            db.session.delete(message)
        db.session.commit()

    if room_unique_id:
        room = c.get_room(room_unique_id)
        c.save_message(
            f"{current_user.name}, how can I assist you? Are you looking to buy or sell a ticket?",
            "Buy",
            room,
        )
    else:
        room = m.Room(
            buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
        ).save()
        c.save_message(
            "Hello! Welcome to FanTicketBot. How can I assist you today? Are you looking to buy or sell a ticket?",
            "Buy",
            room,
        )

    locations = m.Location.all()
    messages = db.session.scalars(room.messages.select())

    return render_template(
        "chat/buy/event_name.html",
        locations=locations,
        now=c.utcnow_chat_format(),
        room=room,
        messages=messages,
    )


@chat_blueprint.route("/home")
def home():
    try:
        params = s.ChatAuthEmailParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.room_unique_id:
        log(log.ERROR, "room_unique_id not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    room = c.get_room(params.room_unique_id)

    if not room:
        log(log.ERROR, "Room not found: [%s]", params.room_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if params.save_history:
        messages_query = m.Message.select().where(m.Message.room_id == room.id)
        messages = db.session.scalars(messages_query).all()

        if current_user.is_authenticated:
            mail_controller.send_email(
                (current_user,),
                f"Today's chat history {datetime.now().strftime(app.config['DATE_CHAT_HISTORY_FORMAT'])}",
                render_template(
                    "email/chat_history.htm",
                    user=current_user,
                    messages=messages,
                ),
            )
            for message in messages:
                db.session.delete(message)
            db.session.commit()

    return render_template(
        "chat/chat_home.html",
        now=c.utcnow_chat_format(),
        room=room,
    )
