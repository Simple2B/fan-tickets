from flask.testing import FlaskClient
from flask_login import current_user
from app import models as m, db
from test_flask.utils import login


def test_chat_window(client: FlaskClient):
    login(client)
    response = client.get("/")
    assert f"Hi, {current_user.name}" in response.data.decode()
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
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save()

    response = client.get("/chat/email?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    TESTING_EMAIL = "new@email.com"
    users_count = len(m.User.all())
    response = client.get(f"/chat/email?room_unique_id={room.unique_id}&email={TESTING_EMAIL}")
    assert response.status_code == 200
    assert len(m.User.all()) == users_count + 1
    assert len(room.messages) == 2


def test_password(client: FlaskClient):
    response = client.get("/chat/password")
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
    test_password = "123456"

    response = client.post(
        "/chat/password",
        data=dict(
            room_unique_id=room.unique_id,
            user_unique_id=user.unique_id,
            password=test_password,
            confirm_password="000000",
        ),
    )
    assert response.status_code == 200
    assert "Passwords do not match" in response.data.decode()

    response = client.post(
        "/chat/password",
        data=dict(
            room_unique_id=room.unique_id,
            user_unique_id=user.unique_id,
            password=test_password,
            confirm_password=test_password,
        ),
    )
    assert response.status_code == 200
    assert "Password has been created" in response.data.decode()
    assert len(room.messages) == 2


def test_create_name(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save()

    response = client.get("/chat/create_name?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    user: m.User = m.User(email="new@gmail.com").save(False)
    db.session.commit()

    TESTING_NAME = "Robert"
    response = client.get(
        f"/chat/create_name?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&name={TESTING_NAME}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 2
    assert user.name == TESTING_NAME
    assert f"Name: {TESTING_NAME}" in response.data.decode()


def test_create_last_name(client: FlaskClient):
    response = client.get("/chat/create_last_name")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    user: m.User = m.User(email="new@gmail.com").save(False)
    db.session.commit()

    TESTING_NAME = "Dickson"
    response = client.get(
        f"/chat/create_name?room_unique_id={room.unique_id}&user_unique_id={user.unique_id}&name={TESTING_NAME}"
    )
    assert response.status_code == 200
    assert len(room.messages) == 2
    assert user.last_name == TESTING_NAME
    assert f"Last name: {TESTING_NAME}" in response.data.decode()


def test_chat_phone(client: FlaskClient):
    response = client.get("/chat/phone")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    user: m.User = m.User(email="new@gmail.com").save(False)
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


def test_chat_home(client: FlaskClient):
    response = client.get("/chat/home")
    assert response.status_code == 200
    assert "Are you looking for buying or selling tickets" in response.data.decode()
