from app.models import User

TEST_ADMIN_NAME = "bob"
TEST_ADMIN_EMAIL = "bob@test.com"
TEST_ADMIN_PASSWORD = "password"
TEST_PHONE = "+380000000012"
TEST_CARD = "0000000000001100"


def register(
    username=TEST_ADMIN_NAME,
    email=TEST_ADMIN_EMAIL,
    password=TEST_ADMIN_PASSWORD,
    phone=TEST_PHONE,
    card=TEST_CARD,
):
    user = User(username=username, email=email)
    user.phone = phone
    user.card = card
    user.password = password
    user.save()
    return user.id


def login(client, username=TEST_ADMIN_NAME, password=TEST_ADMIN_PASSWORD):
    return client.post(
        "/login", data=dict(user_id=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
