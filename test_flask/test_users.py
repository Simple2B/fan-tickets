from flask import current_app as app
from flask_login import current_user
from flask.testing import FlaskClient, FlaskCliRunner
from werkzeug.datastructures import FileStorage
from click.testing import Result
from app import models as m, db
from test_flask.utils import login


def test_list(client_with_data: FlaskClient):
    login(client_with_data)
    DEFAULT_PAGE_SIZE = app.config["DEFAULT_PAGE_SIZE"]
    response = client_with_data.get("/admin/user/users")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    users: list[m.User] = db.session.scalars(m.User.select().order_by(m.User.id).limit(11)).all()
    assert len(users) == 11
    for user in users[:DEFAULT_PAGE_SIZE]:
        assert user.last_name in html
    assert users[10].last_name not in html

    client_with_data.application.config["PAGE_LINKS_NUMBER"] = 6
    response = client_with_data.get("/admin/user/users?page=3")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    assert "/admin/user/users?page=6" in html
    assert "/admin/user/users?page=3" in html
    assert "/admin/user/users?page=10" not in html


def test_create_admin(runner: FlaskCliRunner, client):
    res: Result = runner.invoke(args=["create-admin"])
    assert "admin created" in res.output
    query = m.User.select().where(m.User.username == app.config["ADMIN_USERNAME"])
    assert db.session.scalar(query)


def test_delete_user(client: FlaskClient):
    login(client)
    user: m.User = db.session.scalar(m.User.select())
    response = client.delete("/admin/user/delete/1")
    assert response.status_code == 200
    assert user.activated is False


def test_user_profile(client: FlaskClient):
    login(client)
    response = client.get("profile")
    assert response.status_code == 200
    assert "profile" in response.data.decode()
    assert "Endereço de Email" in response.data.decode()


def test_user_email_edit(client: FlaskClient):
    login(client)
    user: m.User = current_user
    response = client.get("profile")
    assert response.status_code == 200
    assert user.username in response.data.decode()
    assert user.email in response.data.decode()

    response = client.get("/profile/edit_email")
    assert response.status_code == 200

    response = client.post(
        "/profile/save_email",
        data={"email": "new@email.com"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert user.email == "new@email.com"


def test_user_phone_edit(client: FlaskClient):
    login(client)
    user: m.User = current_user
    response = client.get("/profile/edit_phone")
    assert response.status_code == 200

    response = client.post(
        "/profile/save_phone",
        data={"phone": "123456789"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert user.phone == "123456789"


def test_user_card_edit(client: FlaskClient):
    login(client)
    user: m.User = current_user

    response = client.get("/profile/edit_card")
    assert response.status_code == 200

    response = client.post(
        "/profile/save_card",
        data={"card": "0000111122223333"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert user.card == "0000111122223333"
    assert user.activated

    response = client.post(
        "/profile/save_card",
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
        "/profile/set_notifications",
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

    response = client.get("/profile/export")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv; charset=utf-8"
    assert response.headers["Content-Disposition"].startswith("attachment;")
    assert user.username in response.data.decode()
    assert user.email in response.data.decode()


def test_user_deactivate_account(client: FlaskClient):
    login(client)
    user: m.User = current_user

    response = client.get("/profile/deactivate")
    assert response.status_code == 302
    assert user.activated is False


def test_ticket_transfer(client_with_data: FlaskClient):
    login(client_with_data)
    user: m.User = current_user
    ticket: m.Ticket = db.session.scalar(m.Ticket.select().where(m.Ticket.is_sold.is_(True)))
    ticket.buyer_id = user.id
    assert ticket
    payment: m.Payment = db.session.scalar(m.Payment.select().where(m.Payment.ticket_id == ticket.id))
    payment.buyer_id = user.id
    response = client_with_data.get(f"pay/transfer?ticket_unique_id={ticket.unique_id}")
    assert response.status_code == 200
    assert ticket.is_transferred is True


def test_ticket_pdf(client_with_data: FlaskClient):
    login(client_with_data)
    user: m.User = current_user
    room = m.Room(
        seller_id=user.id,
        buyer_id=2,
    ).save()
    ticket: m.Ticket = db.session.scalar(m.Ticket.select())
    ticket.buyer_id = user.id

    with open("test_flask/assets/pagarme/testing_ticket.pdf", "rb") as file:
        file_instance = FileStorage(file)

        data = dict(
            room_unique_id=room.unique_id,
            ticket_unique_id=ticket.unique_id,
            user_unique_id=user.uuid,
            file=[file_instance],
        )

        response = client_with_data.post("/chat/sell/ticket/get_ticket_document", data=data)
        assert response.status_code == 200
        assert b"Done" in response.data
        assert b"You will receive a notification" in response.data

    with open("test_flask/assets/pagarme/testing_ticket.pdf", "rb") as file:
        file_bytes = file.read()
        assert file_bytes == ticket.file

    download_response = client_with_data.get(f"pay/download_pdf?ticket_unique_id={ticket.unique_id}")
    assert download_response.status_code == 200
    assert download_response.headers["Content-Type"] == "application/pdf"
    assert download_response.headers["Content-Disposition"].startswith("attachment;")
    assert download_response.headers["Content-Disposition"].endswith(".pdf")
