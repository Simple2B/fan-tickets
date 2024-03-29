from app.models import User, NotificationsConfig
from app import models as m

TEST_ADMIN_NAME = "bob"
TEST_ADMIN_LAST_NAME = "bobinson"
TEST_ADMIN_EMAIL = "bob@test.com"
TEST_ADMIN_PASSWORD = "password"
TEST_PHONE = "+380000000012"
TEST_CARD = "0000000000001100"


def register(
    username=TEST_ADMIN_NAME,
    name=TEST_ADMIN_NAME,
    last_name=TEST_ADMIN_LAST_NAME,
    email=TEST_ADMIN_EMAIL,
    password=TEST_ADMIN_PASSWORD,
    phone=TEST_PHONE,
    card=TEST_CARD,
    role=m.UserRole.admin.value,
):
    user = User(
        username=username,
        name=name,
        last_name=last_name,
        email=email,
        role=role,
    )
    user.phone = phone
    user.card = card
    user.password = password
    user.activated = True
    user.save()

    NotificationsConfig(user_id=user.id).save()
    return user.id


def login(client, username=TEST_ADMIN_NAME, password=TEST_ADMIN_PASSWORD):
    return client.post("/login", data=dict(user_id=username, password=password), follow_redirects=True)


def logout(client):
    return client.get("/logout", follow_redirects=True)
