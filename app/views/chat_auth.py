import os
from datetime import datetime
from urllib.parse import urlparse
from sqlalchemy import or_

from sqlalchemy.exc import IntegrityError

from flask import request, Blueprint, render_template, current_app as app
from flask_login import current_user, login_user

from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m, db
from app.logger import log
from app import mail_controller
from app.controllers.jinja_globals import transactions_last_month
from config import config

CFG = config()

chat_auth_blueprint = Blueprint("chat", __name__, url_prefix="/chat")


@chat_auth_blueprint.route("/login_form", methods=["GET", "POST"])
def login_form():
    room_unique_id = request.args.get("room_unique_id")
    ticket_unique_id = request.args.get("ticket_unique_id")
    login_from_navbar = request.args.get("login_from_navbar")
    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if login_from_navbar:
        room = m.Room(
            buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
        ).save()

    if not room:
        log(log.ERROR, "Room not found")
        return render_template(
            "chat/registration/00_login_form.html",
            error_message="Room not found",
        )

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    return render_template(
        "chat/registration/00_login_form.html",
        room=room,
        ticket=ticket,
    )


@chat_auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    chat_email = request.args.get("chat_email")
    chat_password = request.args.get("chat_password")
    room_unique_id = request.args.get("room_unique_id")
    ticket_unique_id = request.args.get("ticket_unique_id")

    room_query = m.Room.select().where(m.Room.unique_id == room_unique_id)
    room: m.Room = db.session.scalar(room_query)

    if not room:
        log(log.ERROR, "Room not found")
        return render_template(
            "chat/registration/00_login_form.html",
            error_message="Room not found",
        )

    user: m.User = m.User.authenticate(chat_email, chat_password)
    if not user:
        log(log.ERROR, "Wrong email or password")
        return render_template(
            "chat/registration/00_login_form.html",
            error_message="Wrong email or password",
            room=room,
        )

    login_user(user)
    log(log.INFO, "Login successful.")

    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)
    ticket.is_in_cart = True
    ticket.buyer_id = user.id
    ticket.save()

    cart_tickets_query = m.Ticket.select().where(m.Ticket.buyer == current_user)
    cart_tickets = db.session.scalars(cart_tickets_query).all()
    total_price = sum([ticket.price_gross for ticket in cart_tickets])

    return render_template(
        "chat/buy/tickets_06_cart.html",
        room=room,
        cart_tickets=cart_tickets,
        total_price=total_price,
    )


@chat_auth_blueprint.route("/sell", methods=["GET", "POST"])
def sell():
    seller_id = current_user.id if current_user.is_authenticated else None
    room_unique_id = request.args.get("room_unique_id")
    renew_search = request.args.get("renew_search")
    room = None

    if room_unique_id:
        room = c.get_room(room_unique_id)
        c.save_message(
            "How can I assist you? Are you looking to buy or sell a ticket?",
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
                error_message="You have reached the limit of 6 transactions per month",
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


@chat_auth_blueprint.route("/buy")
def buy():
    room_unique_id = request.args.get("room_unique_id")
    if room_unique_id:
        room = c.get_room(room_unique_id)
        c.save_message(
            "How can I assist you? Are you looking to buy or sell a ticket?",
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


@chat_auth_blueprint.route("/open", methods=["GET", "POST"])
def open():
    return render_template(
        "chat/chat_home.html",
        now=c.utcnow_chat_format(),
    )


@chat_auth_blueprint.route("/close")
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


@chat_auth_blueprint.route("/login_email")
def login_email():
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

    if params.from_sign_up:
        c.save_message("You do not log in. Please log in or sign up", "Sign in", room)
        log(log.INFO, "Sign in from login form")
        return render_template(
            "chat/registration/login_email.html",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    if not params.user_message:
        log(log.ERROR, "No email: [%s]", params.user_message)
        return render_template(
            "chat/registration/login_email.html",
            error_message="Please, add your email",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    user = c.get_user_by_email(params.user_message, room)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_message)
        return render_template(
            "chat/registration/login_email.html",
            error_message="Email not found, add correct email or sign up",
            room=room,
            now=c.utcnow_chat_format(),
            ticket_unique_id=params.ticket_unique_id,
        )

    return render_template(
        "chat/registration/login_password.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.uuid,
        form=f.ChatAuthPasswordForm(),
        ticket_unique_id=params.ticket_unique_id,
    )


@chat_auth_blueprint.route("/login_password", methods=["GET", "POST"])
def login_password():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error: [%s]",
            form.errors,
        )
        return render_template(
            "chat/registration/login_password.html",
            error_message=f"{form.errors}",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            ticket_unique_id=form.ticket_unique_id.data,
            form=form,
        )

    result, user = c.confirm_password(form, room)

    if not result:
        c.save_message("Please enter your password", "Password does not match", room)
        log(log.ERROR, "Password not confirmed: [%s]", form.password.data)
        return render_template(
            "chat/registration/password_confirm.html",
            error_message="Password does not match. Please, inout correct password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            ticket_unique_id=form.ticket_unique_id.data,
            form=form,
        )

    login_user(user)
    log(log.INFO, "Login successful")

    c.save_message("Please enter your password", "You are logged in", room)

    if form.ticket_unique_id.data:
        return render_template(
            "chat/buy/booking_ticket_from_web.html",
            now=c.utcnow_chat_format(),
            room=room,
            ticket_unique_id=form.ticket_unique_id.data,
        )

    return render_template(
        "chat/chat_home.html",
        now=c.utcnow_chat_format(),
        room=room,
    )


@chat_auth_blueprint.route("/reset_registration", methods=["GET"])
def reset_registration():
    params = s.ChatAuthParams.model_validate(dict(request.args))

    room = c.get_room(params.room_unique_id)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        return render_template(
            "chat/email.html",
            now=c.utcnow_chat_format(),
            room=room,
        )

    db.session.delete(user)
    db.session.commit()

    return render_template(
        "chat/registration/email.html",
        now=c.utcnow_chat_format(),
        room=room,
    )


@chat_auth_blueprint.route("/create_user_email")
def create_user_email():
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

    if params.from_sign_up:
        c.save_message("You do not log in. Please log in or sign up", "Sign up", room)
        log(log.INFO, "Sign up from selling")
        return render_template(
            "chat/registration/email.html",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not params.user_message:
        log(log.ERROR, "No email: [%s]", params.user_message)
        return render_template(
            "chat/registration/email.html",
            error_message="Field is empty",
            room=room,
            now=c.utcnow_chat_format(),
        )

    response, user = c.create_email(params.user_message, room)

    if response.is_error:
        return render_template(
            "chat/registration/email.html",
            error_message=response.message,
            room=room,
            now=c.utcnow_chat_format(),
            email_input=response.email,
        )

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_message)
        return render_template(
            "chat/registration/email.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
        )

    try:
        db.session.commit()
        log(log.INFO, f"User {user.email} created")
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User is not created: [%s]", e)
        return render_template(
            "chat/registration/email.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    mail_controller.send_email(
        (user,),
        f"Verify email for {CFG.APP_NAME}",
        render_template(
            "email/email_confirm.htm",
            verification_code=response.verification_code,
        ),
    )

    return render_template(
        "chat/registration/email_confirm.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.uuid,
    )


@chat_auth_blueprint.route("/email_verification")
def email_verification():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()

    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
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

    if not params.user_message:
        log(log.ERROR, "No verification code: [%s]", params.user_message)
        return render_template(
            "chat/registration/email_confirm.html",
            error_message="No verification code, please confirm your email",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            form=form,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if user.verification_code != params.user_message:
        log(log.ERROR, "Wrong verification code: [%s]", params.user_message)
        return render_template(
            "chat/registration/email_confirm.html",
            error_message="Wrong verification code, please confirm your email",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            form=form,
        )

    c.save_message("Please confirm your email", "Email confirmed", room)

    return render_template(
        "chat/registration/password.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.uuid,
        form=form,
    )


@chat_auth_blueprint.route("/create_user_password", methods=["POST"])
def create_user_password():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error: [%s]",
            form.errors,
        )
        return render_template(
            "chat/registration/password.html",
            error_message="You did not add your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    success = c.create_password(form, room)

    try:
        db.session.commit()
        log(log.INFO, "User password added")
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User is not created: [%s]", e)
        return render_template(
            "chat/registration/password.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if not success:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/password.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    return render_template(
        "chat/registration/password_confirm.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=form.user_unique_id.data,
        form=form,
    )


@chat_auth_blueprint.route("/confirm_user_password", methods=["POST"])
def confirm_user_password():
    form: f.ChatAuthPasswordForm = f.ChatAuthPasswordForm()
    form_file = f.ChatFileUploadForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error: [%s]",
            form.errors,
        )
        return render_template(
            "chat/registration/password_confirm.html",
            error_message="Please, confirm your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    result, user = c.confirm_password(form, room)

    if not result:
        c.save_message("Please confirm your password", "Password does not match", room)
        log(log.ERROR, "Password not confirmed: [%s]", form.password.data)
        return render_template(
            "chat/registration/password_confirm.html",
            error_message="Password does not match. Please, confirm your password",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    c.save_message("Please confirm your password", "Password has been confirmed", room)

    return render_template(
        "chat/registration/passport_identity_number.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=form.user_unique_id.data,
        form=form_file,
    )


@chat_auth_blueprint.route("/create_user_passport", methods=["GET", "POST"])
def create_user_passport():
    form: f.ChatFileUploadForm = f.ChatFileUploadForm()

    room = c.get_room(form.room_unique_id.data)

    if not room:
        log(log.ERROR, "Room not found: [%s]", form.room_unique_id.data)
        return render_template(
            "chat/sell/passport.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    if not form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error, user_unique_id: [%s], room_unique_id: [%s]",
            form.user_unique_id.data,
            form.room_unique_id.data,
        )
        return render_template(
            "chat/registration/passport.html",
            error_message="Form submitting error",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    if not form.file.data:
        log(log.ERROR, "No identification document: [%s]", form.file.data)
        return render_template(
            "chat/registration/passport.html",
            error_message="No verification document, please upload your identification document",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    user = c.get_user(form.user_unique_id.data)

    if not user:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )
    if user.identity_document:
        return render_template(
            "chat/registration/passport_identity_number.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    error_message = c.add_identity_document(form, room)

    if error_message:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return render_template(
            "chat/registration/passport.html",
            error_message=error_message,
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=form.user_unique_id.data,
            form=form,
        )

    return render_template(
        "chat/registration/passport_identity_number.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=form.user_unique_id.data,
        form=form,
    )


@chat_auth_blueprint.route("/create_passport_identity_number")
def create_passport_identity_number():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
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

    if not params.user_message:
        log(log.ERROR, "No identity number provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/passport_identity_number.html",
            error_message="Please, add your identity number",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if user.document_identity_number:
        c.save_message("Please input your identification number", f"Identification number: {params.user_message}", room)
        return render_template(
            "chat/registration/name.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    c.add_identity_document_number(params.user_message, user, room)

    return render_template(
        "chat/registration/name.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )


@chat_auth_blueprint.route("/create_user_name")
def create_user_name():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
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

    if not params.user_message:
        log(log.ERROR, "No name provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/name.html",
            error_message="Please, add your name",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    # if user.name:
    #     return render_template(
    #         "chat/registration/last_name.html",
    #         room=room,
    #         now=c.utcnow_chat_format(),
    #         user_unique_id=user.unique_id,
    #     )

    c.create_user_name(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "User name added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User name is not added: [%s]", e)
        return render_template(
            "chat/registration/name.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/registration/last_name.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )


@chat_auth_blueprint.route("/create_user_last_name")
def create_user_last_name():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
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

    if not params.user_message:
        log(log.ERROR, "No last name provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/last_name.html",
            error_message="Please, add your last name",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if user.last_name:
        return render_template(
            "chat/registration/phone.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    c.create_user_last_name(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "User last name added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "User last name is not added: [%s]", e)
        return render_template(
            "chat/registration/last_name.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/registration/phone.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )


@chat_auth_blueprint.route("/create_user_phone")
def create_user_phone():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
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

    if not params.user_message:
        log(log.ERROR, "No last name provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/phone.html",
            error_message="Please, add your phone",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if user.phone:
        return render_template(
            "chat/registration/address.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    error_message = c.create_phone(params.user_message, user, room)

    if error_message:
        log(log.ERROR, error_message)
        return render_template(
            "chat/registration/phone.html",
            error_message=error_message,
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
            phone=params.user_message,
        )

    try:
        db.session.commit()
        log(log.INFO, "Phone added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Phone is not added: [%s]", e)
        return render_template(
            "chat/registration/phone.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    # if current_user.is_authenticated:
    #     return render_template(
    #         "chat/registration/birth_date.html",
    #         room=room,
    #         now=c.utcnow_chat_format(),
    #         user_unique_id=user.unique_id,
    #     )

    # parse url and get the domain name
    if os.environ.get("APP_ENV") == "development":
        parsed_url = urlparse(request.base_url)
        profile_url = f"{parsed_url.scheme}://{parsed_url.netloc}/user/profile"
    else:
        if os.environ.get("SERVER_TYPE") == "production":
            base_url = app.config["PRODUCTION_BASE_URL"]
        else:
            base_url = app.config["STAGING_BASE_URL"]
        profile_url = f"{base_url}user/profile"

    return render_template(
        "chat/registration/address.html",
        now=c.utcnow_chat_format(),
        room=room,
        user_unique_id=user.uuid,
        profile_url=profile_url,
    )


@chat_auth_blueprint.route("/create_user_address")
def create_user_address():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
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

    if not params.user_message:
        log(log.ERROR, "No address provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/address.html",
            error_message="Please, add your address",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if user.address:
        return render_template(
            "chat/registration/birth_date.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    c.create_address(params.user_message, user, room)

    try:
        db.session.commit()
        log(log.INFO, "Address added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Address is not added: [%s]", e)
        return render_template(
            "chat/registration/address.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    return render_template(
        "chat/registration/birth_date.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )


@chat_auth_blueprint.route("/create_user_birth_date")
def create_user_birth_date():
    try:
        params = s.ChatAuthParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
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

    if not params.user_message:
        log(log.ERROR, "No birth date provided: [%s]", params.user_message)
        return render_template(
            "chat/registration/birth_date.html",
            error_message="Please, add your birth date",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    user = c.get_user(params.user_unique_id)

    if not user:
        log(log.ERROR, "User not found: [%s]", params.user_unique_id)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    birth_date_added = c.create_birth_date(params.user_message, user, room)
    if not birth_date_added:
        log(log.ERROR, "Birth date not added: [%s]", params.user_message)
        return render_template(
            "chat/registration/birth_date.html",
            error_message="Wrong date format. Please try again",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=params.user_unique_id,
        )

    try:
        db.session.commit()
        log(log.INFO, "Birth date added: [%s]", params.user_message)
    except IntegrityError as e:
        db.session.rollback()
        log(log.ERROR, "Birth date is not added: [%s]", e)
        return render_template(
            "chat/registration/birth_date.html",
            error_message="Form submitting error. Please add your email again",
            room=room,
            now=c.utcnow_chat_format(),
        )

    if current_user.is_authenticated:
        return render_template(
            "chat/chat_home.html",
            room=room,
            now=c.utcnow_chat_format(),
            user_unique_id=user.uuid,
        )

    return render_template(
        "chat/registration/ask_social_profile.html",
        room=room,
        now=c.utcnow_chat_format(),
        user_unique_id=user.uuid,
    )


@chat_auth_blueprint.route("/create_user_social_profile", methods=["GET", "POST"])
def create_user_social_profile():
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
        c.save_message("You have successfully registered", "Without social profile", room)

        log(log.INFO, f"User: {user.email} logged in")
        return render_template(
            "chat/registration/verified.html",
            room=room,
            now=c.utcnow_chat_format(),
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

    return render_template(
        "chat/registration/verified.html",
        room=room,
        now=c.utcnow_chat_format(),
    )


@chat_auth_blueprint.route("/home")
def home():
    try:
        params = s.ChatRequiredParams.model_validate(dict(request.args))
    except Exception as e:
        log(log.ERROR, "Form submitting error: [%s]", e)
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=c.utcnow_chat_format(),
        )

    if not params.room_unique_id:
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

    return render_template(
        "chat/chat_home.html",
        now=c.utcnow_chat_format(),
        room=room,
    )
