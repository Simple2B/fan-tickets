from datetime import datetime
from bardapi import Bard
from flask import render_template, Blueprint, request
from flask_login import current_user
from app import models as m, db


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return render_template(
        "landing/home/index.html",
    )


@main_blueprint.route("/help")
def help():
    return render_template("help.html")


@main_blueprint.route("/locations")
def get_locations():
    locations = m.Location.all()
    return render_template("demo/locations.html", locations=locations)


@main_blueprint.route("/categories")
def get_categories():
    categories = m.Category.all()
    return render_template("demo/categories.html", categories=categories)


@main_blueprint.route("/events")
def get_events():
    events = m.Event.all()
    return render_template("events/events.html", events=events)


@main_blueprint.route("/tickets")
def get_tickets():
    tickets = m.Ticket.all()
    return render_template("demo/tickets.html", tickets=tickets)


@main_blueprint.route("/reviews")
def get_reviews():
    reviews = m.Review.all()
    return render_template("demo/reviews.html", reviews=reviews)


@main_blueprint.route("/disputes")
def get_disputes():
    disputes = m.Dispute.all()
    return render_template("demo/disputes.html", disputes=disputes)


@main_blueprint.route("/notifications")
def get_notifications():
    notifications = m.Notification.all()
    return render_template("demo/notifications.html", notifications=notifications)


@main_blueprint.route("/room/<room_unique_id>")
def get_room(room_unique_id: str):
    room = db.session.scalar(m.Room.select().where(m.Room.unique_id == room_unique_id))
    return render_template("demo/room.html", room=room)


@main_blueprint.route("/chat")
def chat():
    room = db.session.scalar(m.Room.select().where(m.Room.id == 576))
    messages_query = (
        m.Message.select()
        .where(m.Message.room_id == 576)
        .order_by(m.Message.created_at.asc())
    )
    messages = db.session.scalars(messages_query).all()
    return render_template(
        "demo/chat.html",
        room=room,
        messages=messages,
    )


@main_blueprint.route("/chat", methods=["POST"])
def chat_messages():
    bard = Bard()

    now = datetime.now()
    now_str = now.strftime("%H:%M:%S")
    new_message_text = request.form.get("message")

    m.Message(
        sender_id=current_user.id,
        room_id=576,
        text=new_message_text,
    ).save()

    if new_message_text == "/clear":
        delete_query = m.Message.select().where(m.Message.room_id == 576)
        delete_objects = db.session.scalars(delete_query).all()
        for obj in delete_objects:
            db.session.delete(obj)
            db.session.commit()
    elif new_message_text == "Hi":
        m.Message(
            sender_id=2,
            room_id=576,
            text="Hello from Chatbot!",
        ).save()
    elif new_message_text == "/events":
        events_query = m.Event.select().order_by(m.Event.date_time.desc())
        events = db.session.scalars(events_query).all()
        response = ""
        for event in events:
            response += f"{event.name}\n\n{event.date_time.isoformat()}\n\n"
        m.Message(
            sender_id=2,
            room_id=576,
            text=response,
        ).save()
    else:
        bard_answer = bard.get_answer(new_message_text).get("content")
        m.Message(
            sender_id=2,
            room_id=576,
            text=bard_answer,
        ).save()

    messages_query = (
        m.Message.select()
        .where(m.Message.room_id == 576)
        .order_by(m.Message.created_at.asc())
    )
    messages = db.session.scalars(messages_query).all()

    return render_template(
        "demo/chat_messages.html",
        now=now_str,
        message=new_message_text,
        messages=messages,
    )
