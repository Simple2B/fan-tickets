import os
import pytest
from datetime import datetime
from flask_login import current_user
from flask.testing import FlaskClient
from .utils import login

# from .utils import login
from app.controllers.payments import (
    get_all_pagarme_customers,
    get_pagarme_customer,
    create_pagarme_customer,
    update_pagarme_customer,
    # create_pagarme_card,
    # update_pagarme_card,
    # delete_pagarme_card,
    # create_pagarme_order,
    # create_pagarme_charge,
    # create_pagarme_item,
)


@pytest.mark.skipif(not os.environ.get("PAGARME_CONNECTION"), reason="no pagar.me API secret key")
def test_pagarme_get_customers(client: FlaskClient):
    pagarme_customers = get_all_pagarme_customers()
    assert pagarme_customers


@pytest.mark.skipif(not os.environ.get("PAGARME_CONNECTION"), reason="no pagar.me API secret key")
def test_pagarme_get_customer(client: FlaskClient):
    TESTING_CUSTOMER_ID = "cus_00000000000000"
    pagarme_customer = get_pagarme_customer(TESTING_CUSTOMER_ID)
    assert pagarme_customer
    assert "Customer not found" in pagarme_customer

    # Get real customer id from database
    # Call the function again with the real customer id


@pytest.mark.skipif(not os.environ.get("PAGARME_CONNECTION"), reason="no pagar.me API secret key")
def test_pagarme_create_customer(client: FlaskClient):
    TESTING_BIRTH_DATE = "01/01/2000"
    now = datetime.now().strftime("%m-%d-%H-%M-%S")
    TESTING_CUSTOMER_NAME = f"TestingCustomer {now}"
    created_pagarme_customer = create_pagarme_customer(TESTING_CUSTOMER_NAME, TESTING_BIRTH_DATE)
    assert created_pagarme_customer
    assert created_pagarme_customer.name == TESTING_CUSTOMER_NAME


@pytest.mark.skipif(not os.environ.get("PAGARME_CONNECTION"), reason="no pagar.me API secret key")
def test_pagarme_update_customer(client: FlaskClient):
    TESTING_BIRTH_DATE = "01/01/2000"
    now = datetime.now().strftime("%m-%d-%H-%M-%S")
    TESTING_CUSTOMER_NAME = f"TestingCustomer {now}"
    created_pagarme_customer = create_pagarme_customer(TESTING_CUSTOMER_NAME, TESTING_BIRTH_DATE)
    assert created_pagarme_customer
    assert created_pagarme_customer.name == TESTING_CUSTOMER_NAME

    TESTING_BIRTH_DATE_UPD = "02/02/2000"
    TESTING_NAME_UPD = "UpdatedTestingCustomer"
    updated_pagarme_customer = update_pagarme_customer(
        created_pagarme_customer.id, TESTING_BIRTH_DATE_UPD, TESTING_NAME_UPD
    )
    assert updated_pagarme_customer
    assert updated_pagarme_customer.name == TESTING_NAME_UPD


@pytest.mark.skipif(not os.environ.get("PAGARME_CONNECTION"), reason="no pagar.me API secret key")
def test_pagarme_ticket_order(client: FlaskClient):
    login(client)
    TESTING_USERNAME = current_user.username
    # response = client.get(f"/pay/ticket_order?username={TESTING_USERNAME}&birthdate=01/01/2000")

    data = {
        "username": TESTING_USERNAME,
        "birthdate": "01/01/2000",
        "number": "4242424242424242",
        "exp_month": "01",
        "exp_year": "2025",
        "cvv": "123",
    }
    response = client.post("/pay/ticket_order", data=data)

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["username"] == TESTING_USERNAME
