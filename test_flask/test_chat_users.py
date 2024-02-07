from datetime import datetime
from flask import current_app as app
from flask.testing import FlaskClient
from flask_login import current_user
from app import models as m, db
from test_flask.utils import login, logout


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
    assert len(room.messages) == 2


def test_password(client: FlaskClient):
    response = client.get("/chat/create_user_password")
    assert response.status_code == 405

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
    messages_count = len(room.messages)
    MESSAGES_IN_CHAT = 2

    response = client.post(
        "/chat/create_user_password",
        data=dict(
            room_unique_id=room.unique_id,
            user_unique_id=user.unique_id,
            password=TEST_PASSWORD,
        ),
    )
    messages_count += MESSAGES_IN_CHAT

    assert response.status_code == 200
    assert "Password has been added" in response.data.decode()
    assert len(room.messages) == messages_count

    response = client.post(
        "/chat/confirm_user_password",
        data=dict(
            room_unique_id=room.unique_id,
            user_unique_id=user.unique_id,
            password="000000",
        ),
    )
    messages_count += MESSAGES_IN_CHAT
    assert response.status_code == 200
    assert "Password does not match" in response.data.decode()
    assert len(room.messages) == messages_count

    response = client.post(
        "/chat/confirm_user_password",
        data=dict(
            room_unique_id=room.unique_id,
            user_unique_id=user.unique_id,
            password=TEST_PASSWORD,
        ),
    )
    messages_count += MESSAGES_IN_CHAT

    assert response.status_code == 200
    assert "Password has been confirmed" in response.data.decode()
    assert len(room.messages) == messages_count


def test_create_user_name(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(email="new@gmail.com").save()

    response = client.get(f"/chat/create_user_name?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}")
    assert response.status_code == 200
    assert "Please, add your name" in response.data.decode()

    TESTING_NAME = "Robert"
    response = client.get(
        f"/chat/create_user_name?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&user_message={TESTING_NAME}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 2
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

    response = client.get(
        f"/chat/create_user_last_name?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}"
    )
    assert response.status_code == 200
    assert "Please, add your last name" in response.data.decode()

    TESTING_LAST_NAME = "Dickson"
    response = client.get(
        f"/chat/create_user_last_name?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&user_message={TESTING_LAST_NAME}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 2
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

    response = client.get(f"/chat/create_user_phone?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}")
    assert response.status_code == 200
    assert "Please, add your phone" in response.data.decode()

    TESTING_PHONE = "380000000000"
    response = client.get(
        f"/chat/create_user_phone?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&user_message={TESTING_PHONE}"
    )
    assert response.status_code == 200
    assert f"Phone: {TESTING_PHONE}" in response.data.decode()
    assert len(room.messages) == 2
    assert user.phone == TESTING_PHONE


def test_create_user_birth_date(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(email="new@gmail.com").save()

    response = client.get(f"/chat/create_user_birth_date?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    response = client.get(
        f"/chat/create_user_birth_date?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}"
    )
    assert response.status_code == 200
    assert "Please, add your birth date" in response.data.decode()

    TESTING_BIRTH_DATE = "22/10/1990"
    response = client.get(
        f"/chat/create_user_birth_date?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&user_message={TESTING_BIRTH_DATE}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 2
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

    response = client.get(f"/chat/create_user_address?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}")
    assert response.status_code == 200
    assert "Please, add your address" in response.data.decode()

    TESTING_ADDRESS = "Street 1"
    response = client.get(
        f"/chat/create_user_address?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&user_message={TESTING_ADDRESS}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 2
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
        f"/chat/create_user_social_profile?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&facebook={True}&user_message={TESTING_FACEBOOK}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 2
    assert user.facebook == TESTING_FACEBOOK
    assert "Facebook url added" in response.data.decode()

    response = client.get(
        f"/chat/create_user_social_profile?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&instagram={True}&user_message={TESTING_INSTAGRAM}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 4
    assert user.instagram == TESTING_INSTAGRAM
    assert "Instagram url added" in response.data.decode()

    response = client.get(
        f"/chat/create_user_social_profile?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&twitter={True}&user_message={TESTING_TWITTER}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 7
    assert user.twitter == TESTING_TWITTER
    assert "Twitter url added" in response.data.decode()
    assert "You have successfully registered" in response.data.decode()
    assert user.email == current_user.email

    logout(client)
    response = client.get(
        f"/chat/create_user_social_profile?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&without_social_profile={True}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 9
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
