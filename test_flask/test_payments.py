import os
import pytest

# from datetime import datetime
import random
import string
from flask_login import current_user
from flask.testing import FlaskClient
from app import schema as s
from .utils import login

# from .utils import login
from app.controllers.payments import (
    get_all_pagarme_customers,
    get_pagarme_customer,
    # update_pagarme_customer,
    get_pagarme_card,
)


# @pytest.mark.skipif(not os.environ.get("PAGARME_CONNECTION"), reason="no pagar.me API secret key")
@pytest.mark.skipif(not os.environ.get("APP_ENV") == "testing", reason="no pagar.me API secret key")
def test_pagarme_get_customers(client: FlaskClient):
    response = get_all_pagarme_customers()
    assert response["data"][0]["id"] == "cus_rwLbRMDIjIz5vy6d"


@pytest.mark.skipif(not os.environ.get("APP_ENV") == "testing", reason="no pagar.me API secret key")
def test_pagarme_get_customer(client: FlaskClient):
    # Fake customer
    TESTING_CUSTOMER_ID = "cus_00000000000000"
    response = get_pagarme_customer(TESTING_CUSTOMER_ID)
    assert response

    if isinstance(response, s.PagarmeError):
        assert response.status_code == 404
        assert response.error == "Customer not found"

    # Real customer
    TESTING_CUSTOMER_ID = "cus_rwLbRMDIjIz5vy6d"
    response = get_pagarme_customer(TESTING_CUSTOMER_ID)
    assert response
    if isinstance(response, s.PagarmeCustomerOutput):
        assert response.id == TESTING_CUSTOMER_ID


@pytest.mark.skipif(not os.environ.get("APP_ENV") == "testing", reason="no pagar.me API secret key")
def test_pagarme_get_card(client: FlaskClient):
    login(client)
    TEST_CUSTOMER_ID = "cus_rwLbRMDIjIz5vy6d"
    TEST_CARD_ID = "card_B1xW3aLTQT629gbX"
    response = get_pagarme_card(TEST_CUSTOMER_ID, TEST_CARD_ID)
    assert response
    assert response.id == TEST_CARD_ID
    assert response.customer.id == TEST_CUSTOMER_ID


@pytest.mark.skipif(not os.environ.get("APP_ENV") == "testing", reason="no pagar.me API secret key")
def test_pagarme_ticket_order(client: FlaskClient):
    login(client)
    letters = string.ascii_lowercase
    TESTING_USERNAME_ID = "".join(random.choice(letters) for _ in range(7))
    TESTING_USERNAME = f"{current_user.username} {TESTING_USERNAME_ID}"
    TESTING_BIRTHDATE = "01/01/2000"

    current_user.billing_line_1 = "Rua Teste"
    current_user.billing_line_2 = "Teste"
    current_user.billing_zip_code = "00000000"
    current_user.billing_city = "City Teste"
    current_user.billing_state = "RJ"
    current_user.billing_country = "BR"
    current_user.save()

    data = {
        "user_unique_id": current_user.unique_id,
        "username": TESTING_USERNAME,
        "birthdate": TESTING_BIRTHDATE,
        "code": current_user.unique_id,
        "email": current_user.email,
        "document": "93095135270",
        "phone": random.randint(100000000, 999999999),
        "card_number": "4242424242424242",
        "exp_month": "01",
        "exp_year": "2025",
        "cvv": "123",
        "item_amount": "1000",
        "item_code": current_user.unique_id,  # replace by ticket's unique_id
        "item_description": "Testing Concert Ticket",
        "item_quantity": "2",
        "item_category": "Testing Concert Event",  # ticket.event.category
    }

    data["payment_method"] = "credit_card"
    response = client.post("/pay/ticket_order", data=data)

    assert response.status_code == 200
    if isinstance(response.json, dict):
        assert response.json["status"] == "approved"

    data["payment_method"] = "pix"
    response = client.post("/pay/ticket_order", data=data)

    assert response.status_code == 200
    if isinstance(response.json, dict):
        assert response.json["status"] == "approved"
