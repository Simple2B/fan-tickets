from datetime import datetime
from random import randint
import re

import sqlalchemy as sa

from flask import current_app as app
from werkzeug.security import check_password_hash

from app.database import db
from app import controllers as c
from app import schema as s
from app import forms as f
from app import models as m


from app.logger import log


def get_user(user_unique_id: str) -> m.User | None:
    user_query = sa.select(m.User).where(m.User.unique_id == user_unique_id)
    user = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", user_unique_id)

    return user


def create_email(email: str, room: m.Room) -> tuple[s.ChatAuthEmailValidate, m.User | None]:
    email = email.strip().lower()
    match_pattern = re.search(app.config["PATTERN_EMAIL"], email)

    if not match_pattern:
        return s.ChatAuthEmailValidate(email=email, message="Invalid email format", is_error=True), None

    user_email_query = sa.select(m.User).where(m.User.email == email)
    user_email = db.session.scalar(user_email_query)

    if user_email:
        return s.ChatAuthEmailValidate(email=email, message="Email already taken", is_error=True), None

    picture_query = m.Picture.select().where(m.Picture.filename.ilike(f"%{'default_avatar'}%"))
    picture: m.Picture = db.session.scalar(picture_query)
    identity_document_query = m.Picture.select().where(m.Picture.filename.ilike(f"%{'default_passport'}%"))
    identity_document = db.session.scalar(identity_document_query)
    picture_id = picture.id if picture else None
    identity_document_id = identity_document.id if identity_document else None
    verification_code = randint(100000, 999999)

    user = m.User(
        # Since in chat registration we get user's info step by step,
        # asking user to input credentials one by one,
        # we need to fill the rest of the fields with default values
        picture_id=picture_id,
        identity_document_id=identity_document_id,
        email=email,
        phone=app.config["CHAT_DEFAULT_PHONE"],
        card=app.config["CHAT_DEFAULT_CARD"],
        password="",
        verification_code=verification_code,
    ).save(False)

    db.session.flush()
    room.seller_id = user.id

    c.save_message("Please input your email", f"Email: {email}", room)

    return s.ChatAuthEmailValidate(email=email, verification_code=verification_code), user


def create_password(form: f.ChatAuthPasswordForm, room: m.Room) -> bool:
    user_query = sa.select(m.User).where(m.User.unique_id == form.user_unique_id.data)
    user = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return False

    user.password = form.password.data
    user.save(False)

    c.save_message("Please input your password", "Password has been added", room)

    return True


def confirm_password(form: f.ChatAuthPasswordForm, room: m.Room) -> tuple[bool, m.User | None]:
    user_query = sa.select(m.User).where(m.User.unique_id == form.user_unique_id.data)
    user = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return False, user

    result = check_password_hash(user.password, form.password.data)

    return result, user


def add_identity_document(form: f.ChatFileUploadForm, room: m.Room) -> str:
    user_query = sa.select(m.User).where(m.User.unique_id == form.user_unique_id.data)
    user = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", form.user_unique_id.data)
        return "Form submitting error"

    response = c.image_upload(user, c.ImageType.IDENTIFICATION)

    if 200 not in response:
        return "Not valid type of verification document, please upload your identification document with right format"

    c.save_message("Please upload your identification document", "Identification document has been uploaded", room)

    return ""


def create_user_name(name: str, user: m.User, room: m.Room):
    user.name = name
    user.save(False)

    c.save_message("Please input your name", f"Name: {name}", room)


def create_user_last_name(last_name: str, user: m.User, room: m.Room):
    user.last_name = last_name
    user.save(False)

    c.save_message("Please input your last name", f"Last name: {last_name}", room)


def create_phone(phone: str, user: m.User, room: m.Room) -> str:
    match_pattern = re.search(app.config["PATTERN_PHONE"], str(phone))

    if not match_pattern:
        return "Invalid phone format"

    user_phone_query = sa.select(m.User).where(m.User.phone == phone)
    user_phone = db.session.scalar(user_phone_query)

    if user_phone:
        return "Phone already taken"

    user.phone = phone
    user.save(False)

    c.save_message("Please input your phone", f"Phone: {phone}", room)

    return ""


def create_address(address: str, user: m.User, room: m.Room):
    user.address = address
    # TODO: Move to birth_date route when it will be added
    user.activated = True
    user.save(False)

    c.save_message("Please input your address", f"Address: {address}", room)


def create_birth_date(birth_date: str, user: m.User, room: m.Room):
    user.birth_date = datetime.strptime(birth_date, app.config["DATE_PICKER_FORMAT"])
    user.activated = True
    user.save(False)

    c.save_message("Please input your birth date", f"Birth date: {birth_date}", room)


def create_social_profile(params: s.ChatAuthSocialProfileParams, user: m.User, room: m.Room):
    message = ""

    if params.facebook:
        user.facebook = params.user_message
        message = "Facebook url added"
    if params.instagram:
        user.instagram = params.user_message
        message = "Instagram url added"
    if params.twitter:
        user.twitter = params.user_message
        message = "Twitter url added"

    c.save_message("Please add your social profiles", message, room)


def get_user_by_email(email: str, room: m.Room) -> m.User | None:
    user_query = sa.select(m.User).where(m.User.email == email)
    user = db.session.scalar(user_query)

    if not user:
        log(log.ERROR, "User not found: [%s]", email)

    c.save_message("To sign in, please input your email", f"{email}", room)

    return user
