from flask.testing import FlaskClient
from flask_login import current_user
from app import models as m, db
from test_flask.utils import login


def test_chat_window(client: FlaskClient):
    login(client)
    response = client.get("/")
    assert f"Hi, {current_user.username}" in response.data.decode()
    assert "Are you looking for buying or selling tickets?" in response.data.decode()


def test_chat_sell(client: FlaskClient):
    TESTING_ROOMS_NUMBER = 1
    TESTING_MESSAGES_NUMBER = 2
    response = client.get("/chat/sell")
    assert response.status_code == 200
    assert len(m.Room.all()) == TESTING_ROOMS_NUMBER
    assert len(m.Message.all()) == TESTING_MESSAGES_NUMBER


def test_chat_username(client: FlaskClient):
    response = client.get("/chat/username?room_unique_id=1&chat_username=TestUser")
    assert response.status_code == 200
    assert "Room not found" in response.data.decode()

    response = client.get("/chat/username?chat_username=TestUser")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save()

    users_count = len(m.User.all())
    response = client.get(f"/chat/username?room_unique_id={room.unique_id}&chat_username=TestUser")
    assert response.status_code == 200
    assert len(room.messages) == 3
    assert len(m.User.all()) == users_count + 1


def test_chat_email(client: FlaskClient):
    response = client.get("/chat/email")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    user = m.User(
        username="testing_user_name",
        email="empty@email.com",
        phone="00000000000",
        card="0000000000000000",
        password="",
    ).save(False)
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    db.session.commit()

    TESTING_EMAIL = "new@email.com"
    response = client.get(
        f"/chat/email?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&chat_email={TESTING_EMAIL}"
    )
    assert response.status_code == 200
    assert user.email == TESTING_EMAIL


def test_chat_phone(client: FlaskClient):
    response = client.get("/chat/phone")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    user = m.User(
        username="testing_user_name",
        email="",
        phone="",
        card="0000000000000000",
        password="",
    ).save(False)
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    db.session.commit()

    TESTING_PHONE = "380000000000"
    response = client.get(
        f"/chat/phone?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&chat_phone={TESTING_PHONE}"
    )
    assert response.status_code == 200
    assert user.phone == TESTING_PHONE
