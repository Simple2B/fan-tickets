from flask import current_app as app
from flask_login import current_user
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import models as m, db
from test_flask.utils import login


def test_list(client_with_data: FlaskClient):
    login(client_with_data)
    DEFAULT_PAGE_SIZE = app.config["DEFAULT_PAGE_SIZE"]
    response = client_with_data.get("/user/")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    users = db.session.scalars(m.User.select().order_by(m.User.id).limit(11)).all()
    assert len(users) == 11
    for user in users[:DEFAULT_PAGE_SIZE]:
        assert user.username in html
    assert users[10].username not in html

    client_with_data.application.config["PAGE_LINKS_NUMBER"] = 6
    response = client_with_data.get("/user/?page=6")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    assert "/user/?page=6" in html
    assert "/user/?page=3" in html
    assert "/user/?page=10" not in html


def test_create_admin(runner: FlaskCliRunner):
    res: Result = runner.invoke(args=["create-admin"])
    assert "admin created" in res.output
    query = m.User.select().where(m.User.username == app.config["ADMIN_USERNAME"])
    assert db.session.scalar(query)


def test_delete_user(client: FlaskClient):
    login(client)
    user: m.User = db.session.scalar(m.User.select())
    response = client.delete("/user/delete/1")
    assert response.status_code == 200
    assert user.activated is False


def test_user_profile(client: FlaskClient):
    login(client)
    response = client.get("/user/profile")
    assert response.status_code == 200
    assert "profile" in response.data.decode()
    assert "Endereço de Email" in response.data.decode()


def test_user_email_edit(client: FlaskClient):
    login(client)
    user: m.User = current_user
    response = client.get("/user/profile")
    assert response.status_code == 200
    assert user.username in response.data.decode()
    assert user.email in response.data.decode()

    response = client.get("/user/edit_email")
    assert response.status_code == 200

    response = client.post(
        "/user/save_email",
        data={"email": "new@email.com"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert user.email == "new@email.com"


def test_user_phone_edit(client: FlaskClient):
    login(client)
    user: m.User = current_user
    response = client.get("/user/edit_phone")
    assert response.status_code == 200

    response = client.post(
        "/user/save_phone",
        data={"phone": "123456789"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert user.phone == "123456789"


def test_user_card_edit(client: FlaskClient):
    login(client)
    user: m.User = current_user

    response = client.get("/user/edit_card")
    assert response.status_code == 200

    response = client.post(
        "/user/save_card",
        data={"card": "0000111122223333"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert user.card == "0000111122223333"
    assert user.activated

    response = client.post(
        "/user/save_card",
        data={"card": "1"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert user.activated is False


def test_user_notifications_edit(client: FlaskClient):
    login(client)
    user: m.User = current_user
    assert user.notifications_config.new_event
    assert user.notifications_config.new_ticket
    assert user.notifications_config.new_message
    assert user.notifications_config.new_buyers_payment
    assert user.notifications_config.your_payment_received
    assert user.notifications_config.ticket_transfer_confirmed
    assert user.notifications_config.dispute_started
    assert user.notifications_config.dispute_resolved

    notification_data = dict(
        new_message=True,
        new_buyers_payment=True,
    )
    response = client.post(
        "/user/set_notifications",
        data=notification_data,
        follow_redirects=True,
    )
    assert response.status_code == 200

    assert not user.notifications_config.new_event
    assert not user.notifications_config.new_ticket
    assert user.notifications_config.new_message
    assert user.notifications_config.new_buyers_payment
    assert not user.notifications_config.your_payment_received
    assert not user.notifications_config.ticket_transfer_confirmed
    assert not user.notifications_config.dispute_started
    assert not user.notifications_config.dispute_resolved


def test_user_export_data(client: FlaskClient):
    login(client)
    user: m.User = current_user

    response = client.get("/user/export")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv; charset=utf-8"
    assert response.headers["Content-Disposition"].startswith("attachment;")
    assert user.username in response.data.decode()
    assert user.email in response.data.decode()


def test_user_deactivate_account(client: FlaskClient):
    login(client)
    user: m.User = current_user

    response = client.get("/user/deactivate")
    assert response.status_code == 302
    assert user.activated is False
