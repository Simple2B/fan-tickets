from flask.testing import FlaskClient
from .utils import login
from app.controllers.payments import (
    get_pagarme_customers,
    get_pagarme_customer,
    create_pagarme_customer,
    update_pagarme_customer,
    create_pagarme_card,
    update_pagarme_card,
    delete_pagarme_card,
    create_pagarme_order,
    create_pagarme_charge,
    create_pagarme_item,
)


def test_pagarme_get_customers(client: FlaskClient):
    pagarme_customers = get_pagarme_customers()
    assert pagarme_customers


def test_pagarme_get_customer(client: FlaskClient):
    pagarme_customer = get_pagarme_customer()
    assert pagarme_customer


def test_pagarme_create_customer(client: FlaskClient):
    TESTING_BIRTH_DATE = "01/01/2000"
    created_pagarme_customer = create_pagarme_customer(TESTING_BIRTH_DATE)
    assert created_pagarme_customer


def test_pagarme_update_customer(client: FlaskClient):
    TESTING_BIRTH_DATE_UPD = "02/02/2000"
    updated_pagarme_customer = update_pagarme_customer(TESTING_BIRTH_DATE_UPD)
    assert updated_pagarme_customer


def test_pagarme_create_card(client: FlaskClient):
    login(client)
    response = client.post("/pay/create_card")
    assert response.status_code == 200
    assert response.json == {"status": "success"}


def test_pagarme_update_card(client: FlaskClient):
    login(client)
    response = client.post("/pay/update_card")
    assert response.status_code == 200
    assert response.json == {"status": "success"}


def test_pagarme_delete_card(client: FlaskClient):
    login(client)
    response = client.post("/pay/delete_card")
    assert response.status_code == 200
    assert response.json == {"status": "success"}


def test_pagarme_create_order(client: FlaskClient):
    login(client)
    response = client.post("/pay/create_order")
    assert response.status_code == 200
    assert response.json == {"status": "success"}


def test_pagarme_create_item(client: FlaskClient):
    login(client)
    response = client.post("/pay/create_item")
    assert response.status_code == 200
    assert response.json == {"status": "success"}


def test_pagarme_webhook(client: FlaskClient):
    response = client.post("/pay/webhook")
    assert response.status_code == 200
    assert response.json == {"status": "success"}
