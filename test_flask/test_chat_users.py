from datetime import datetime, timedelta
from flask import current_app as app
from flask.testing import FlaskClient
from flask_login import current_user
from app import models as m, db
from app.controllers.jinja_globals import transactions_last_month
from test_flask.utils import login, logout
from .db import get_testing_tickets


def test_chat_window(client: FlaskClient):
    login(client)
    response = client.get("/")
    assert "Hello! Welcome to FanTicketBot" in response.data.decode()


def test_chat_sell(client: FlaskClient):
    TESTING_ROOMS_NUMBER = 1
    TESTING_MESSAGES_NUMBER = 2
    response = client.get("/chat/sell")
    assert response.status_code == 200
    assert len(m.Room.all()) == TESTING_ROOMS_NUMBER
    assert len(m.Message.all()) == TESTING_MESSAGES_NUMBER


def test_create_user_email(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save()

    response = client.get(f"/chat/create_user_email?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Field is empty" in response.data.decode()

    TESTING_EMAIL = "new@email.com"
    users_count = len(m.User.all())
    response = client.get(f"/chat/create_user_email?room_unique_id={room.unique_id}&user_message={TESTING_EMAIL}")
    assert response.status_code == 200
    assert len(m.User.all()) == users_count + 1
    assert len(db.session.scalars(room.messages.select()).all()) == 2


def test_password(client_with_data: FlaskClient):
    response = client_with_data.get("/chat/create_user_password")
    assert response.status_code == 405
    ticket: m.Ticket = db.session.scalar(m.Ticket.select())

    TESTING_EMAIL = "new@email.com"
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(
        email=TESTING_EMAIL,
    ).save(False)
    db.session.commit()
    TEST_PASSWORD = "123456"
    messages_count = len(db.session.scalars(room.messages.select()).all())
    MESSAGES_IN_CHAT = 2

    response = client_with_data.post(
        "/chat/create_user_password",
        data=dict(
            room_unique_id=room.unique_id,
            user_unique_id=user.uuid,
            password=TEST_PASSWORD,
            ticket_unique_id=ticket.unique_id,
        ),
    )
    messages_count += MESSAGES_IN_CHAT

    assert response.status_code == 200
    assert "Password has been added" in response.data.decode()
    assert len(db.session.scalars(room.messages.select()).all()) == messages_count

    response = client_with_data.post(
        "/chat/confirm_user_password",
        data=dict(
            room_unique_id=room.unique_id,
            user_unique_id=user.uuid,
            password="000000",
            ticket_unique_id=ticket.unique_id,
        ),
    )
    messages_count += MESSAGES_IN_CHAT
    assert response.status_code == 200
    assert "Password does not match" in response.data.decode()
    assert len(db.session.scalars(room.messages.select()).all()) == messages_count

    response = client_with_data.post(
        "/chat/confirm_user_password",
        data=dict(
            room_unique_id=room.unique_id,
            user_unique_id=user.uuid,
            password=TEST_PASSWORD,
            ticket_unique_id=ticket.unique_id,
        ),
    )
    messages_count += MESSAGES_IN_CHAT

    assert response.status_code == 200
    assert "Password has been confirmed" in response.data.decode()
    assert len(db.session.scalars(room.messages.select()).all()) == messages_count


def test_create_user_name(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(email="new@gmail.com").save()

    response = client.get(f"/chat/create_user_name?room_unique_id={room.unique_id}&user_unique_id={user.uuid}")
    assert response.status_code == 200
    assert "Please, add your name" in response.data.decode()

    TESTING_NAME = "Robert"
    response = client.get(
        f"/chat/create_user_name?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&user_message={TESTING_NAME}"
    )
    assert response.status_code == 200
    assert len(db.session.scalars(room.messages.select()).all()) == 2
    assert user.name == TESTING_NAME
    assert f"Name: {TESTING_NAME}" in response.data.decode()


def test_create_user_last_name(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(email="new@gmail.com").save()

    response = client.get(f"/chat/create_user_last_name?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    response = client.get(f"/chat/create_user_last_name?room_unique_id={room.unique_id}&user_unique_id={user.uuid}")
    assert response.status_code == 200
    assert "Please, add your last name" in response.data.decode()

    TESTING_LAST_NAME = "Dickson"
    response = client.get(
        f"/chat/create_user_last_name?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&user_message={TESTING_LAST_NAME}"
    )
    assert response.status_code == 200
    assert len(db.session.scalars(room.messages.select()).all()) == 2
    assert user.last_name == TESTING_LAST_NAME
    assert f"Last name: {TESTING_LAST_NAME}" in response.data.decode()


def test_create_user_phone(client: FlaskClient):
    user: m.User = m.User(email="new@gmail.com").save(False)
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save()

    response = client.get(f"/chat/create_user_phone?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    response = client.get(f"/chat/create_user_phone?room_unique_id={room.unique_id}&user_unique_id={user.uuid}")
    assert response.status_code == 200
    assert "Please, add your phone" in response.data.decode()

    TESTING_PHONE = "+55-11-11223344"
    response = client.get(
        f"/chat/create_user_phone?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&user_message={TESTING_PHONE}"
    )
    assert response.status_code == 200
    assert "Phone: " in response.data.decode()
    assert TESTING_PHONE[1:] in response.data.decode()
    assert "Please input your address" in response.data.decode()
    assert len(db.session.scalars(room.messages.select()).all()) == 2
    assert user.phone == TESTING_PHONE[1:]


def test_create_user_birth_date(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(email="new@gmail.com").save()

    response = client.get(f"/chat/create_user_birth_date?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    response = client.get(f"/chat/create_user_birth_date?room_unique_id={room.unique_id}&user_unique_id={user.uuid}")
    assert response.status_code == 200
    assert "Please, add your birth date" in response.data.decode()

    TESTING_BIRTH_DATE = "22/10/1990"
    response = client.get(
        f"/chat/create_user_birth_date?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&user_message={TESTING_BIRTH_DATE}"
    )
    assert response.status_code == 200
    assert len(db.session.scalars(room.messages.select()).all()) == 2
    assert user.birth_date == datetime.strptime(TESTING_BIRTH_DATE, app.config["CHAT_USER_FORMAT"])
    assert f"Birth date: {TESTING_BIRTH_DATE}" in response.data.decode()


def test_create_user_address(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(email="new@gmail.com").save()

    response = client.get(f"/chat/create_user_address?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    response = client.get(f"/chat/create_user_address?room_unique_id={room.unique_id}&user_unique_id={user.uuid}")
    assert response.status_code == 200
    assert "Please, add your address" in response.data.decode()

    TESTING_ADDRESS = "Street 1"
    response = client.get(
        f"/chat/create_user_address?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&user_message={TESTING_ADDRESS}"
    )
    assert response.status_code == 200
    assert len(db.session.scalars(room.messages.select()).all()) == 2
    assert user.address == TESTING_ADDRESS
    assert f"Address: {TESTING_ADDRESS}" in response.data.decode()


def test_create_user_social_profile(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(email="new@gmail.com").save()

    response = client.get(f"/chat/create_user_social_profile?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    TESTING_FACEBOOK = "https://www.facebook.com/profile/1"
    TESTING_INSTAGRAM = "https://www.instagram.com/profile/1"
    TESTING_TWITTER = "https://www.twitter.com/profile/1"
    response = client.get(
        f"/chat/create_user_social_profile?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&facebook={True}&user_message={TESTING_FACEBOOK}"
    )
    assert response.status_code == 200
    assert len(db.session.scalars(room.messages.select()).all()) == 2
    assert user.facebook == TESTING_FACEBOOK
    assert "Facebook url added" in response.data.decode()

    response = client.get(
        f"/chat/create_user_social_profile?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&instagram={True}&user_message={TESTING_INSTAGRAM}"
    )
    assert response.status_code == 200
    assert len(db.session.scalars(room.messages.select()).all()) == 4
    assert user.instagram == TESTING_INSTAGRAM
    assert "Instagram url added" in response.data.decode()

    response = client.get(
        f"/chat/create_user_social_profile?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&twitter={True}&user_message={TESTING_TWITTER}"
    )
    assert response.status_code == 200
    assert len(db.session.scalars(room.messages.select()).all()) == 7
    assert user.twitter == TESTING_TWITTER
    assert "Twitter url added" in response.data.decode()
    assert "You have successfully registered" in response.data.decode()
    assert user.email == current_user.email

    logout(client)
    response = client.get(
        f"/chat/create_user_social_profile?room_unique_id={room.unique_id}&user_unique_id={user.uuid}&without_social_profile={True}"
    )
    assert response.status_code == 200
    assert len(db.session.scalars(room.messages.select()).all()) == 9
    assert "You have successfully registered" in response.data.decode()
    assert "Without social profile" in response.data.decode()
    assert user.email == current_user.email


def test_chat_home(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save()
    response = client.get(f"/chat/home?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Are you looking to buy or sell a ticket?" in response.data.decode()


def test_get_testing_tickets(client: FlaskClient):
    login(client)
    user: m.User = current_user

    TESTING_EVENTS_NUMBER = 2
    TESTING_TICKETS_NUMBER = 3
    testing_tickets = get_testing_tickets(user, TESTING_EVENTS_NUMBER, TESTING_TICKETS_NUMBER)

    assert len(testing_tickets) == TESTING_TICKETS_NUMBER * TESTING_EVENTS_NUMBER

    events: list[m.Event] = db.session.scalars(m.Event.select()).all()
    assert len(events) == TESTING_EVENTS_NUMBER


def test_transactions_limit_per_user(client: FlaskClient):
    login(client)
    user: m.User = current_user

    get_testing_tickets(user)

    last_month_tickets_query = m.Ticket.select().where(
        m.Ticket.last_reservation_time > datetime.now() - timedelta(days=30)
    )
    last_month_tickets: list[m.Ticket] = db.session.scalars(last_month_tickets_query).all()
    assert last_month_tickets

    users_transactions_last_month = transactions_last_month(user)
    assert users_transactions_last_month == len(last_month_tickets)

    m.GlobalFeeSettings().save()

    room = m.Room(
        seller_id=user.id,
        buyer_id=2,
    ).save()

    response = client.get(f"/sell/get_event_category?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert b"You have reached the limit of 6 transactions per month" in response.data


def test_transactions_per_event(client: FlaskClient):
    login(client)
    user: m.User = current_user

    TESTING_EVENTS_NUMBER = 1
    TESTING_TICKETS_NUMBER = 3
    testing_tickets = get_testing_tickets(user, TESTING_EVENTS_NUMBER, TESTING_TICKETS_NUMBER)

    assert len(testing_tickets) == TESTING_TICKETS_NUMBER

    m.GlobalFeeSettings(limit_per_event=2).save()

    room = m.Room(
        seller_id=user.id,
        buyer_id=2,
    ).save()

    ticket = testing_tickets[0]
    response = client.get(f"/buy/booking_ticket?room_unique_id={room.unique_id}&ticket_unique_id={ticket.unique_id}")
    assert response.status_code == 200
    assert b"You have reached the limit of tickets for this event" in response.data


"""
http://127.0.0.1:5005/chat/email_verification?ticket_unique_id=60921333-2009-4a19-9790-a9df167aeba7&ticket_unique_id=60921333-2009-4a19-9790-a9df167aeba7&user_unique_id=&user_unique_id=ab1c7027-83c6-4edd-89d3-5daa709391bf&user_unique_id=ab1c7027-83c6-4edd-89d3-5daa709391bf&room_unique_id=300a78b1-eeee-41d5-8d25-17993ae21249&room_unique_id=300a78b1-eeee-41d5-8d25-17993ae21249&user_message=708108
http://127.0.0.1:5005/chat/email_verification?ticket_unique_id=60921333-2009-4a19-9790-a9df167aeba7&ticket_unique_id=60921333-2009-4a19-9790-a9df167aeba7&user_unique_id=&room_unique_id=8595e049-f084-4013-aec3-df72f798b651&user_message=275787
"""
