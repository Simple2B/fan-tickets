import os
import pytest
import random
from datetime import datetime, timedelta
import random
import string
from flask_login import current_user
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import schema as s, models as m, db
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


@pytest.mark.skipif(True, reason="no pagar.me API secret key")
def test_pagarme_ticket_order(client: FlaskClient):
    login(client)
    letters = string.ascii_lowercase
    TESTING_USERNAME_ID = "".join(random.choice(letters) for _ in range(7))
    TESTING_USERNAME = f"{current_user.username} {TESTING_USERNAME_ID}"
    TESTING_BIRTHDATE = "01/01/2000"

    current_user.pagarme_id = "cus_LD8jWxauYfOm9yEe"
    current_user.billing_line_1 = "Rua Teste"
    current_user.billing_line_2 = "Teste"
    current_user.billing_zip_code = "00000000"
    current_user.billing_city = "City Teste"
    current_user.billing_state = "RJ"
    current_user.billing_country = "BR"
    current_user.save()

    room = m.Room(buyer_id=current_user.id).save()

    data = {
        "room_unique_id": room.unique_id,
        "user_unique_id": current_user.uuid,
        "username": TESTING_USERNAME,
        "birthdate": TESTING_BIRTHDATE,
        "code": current_user.uuid,
        "email": current_user.email,
        "document_identity_number": "93095135270",
        "expire": "01/25",
        "phone": random.randint(100000000, 999999999),
        "card_number": "4242424242424242",
        "exp_month": "01",
        "exp_year": "2025",
        "cvv": "123",
        "item_amount": "1000",
        "item_code": current_user.uuid,  # replace by ticket's unique_id
        "item_description": "Testing Concert Ticket",
        "item_quantity": "2",
        "item_category": "Testing Concert Event",  # ticket.event.category
    }

    response = client.post("/pay/ticket_order?payment_method=credit_card", data=data)

    assert response.status_code == 200
    if isinstance(response.json, dict):
        assert response.json["status"] == "approved"

    response = client.post("/pay/ticket_order?payment_method=pix", data=data)

    assert response.status_code == 200
    if isinstance(response.json, dict):
        assert response.json["status"] == "approved"


def test_pay_sellers(runner: FlaskCliRunner):
    command_output: Result = runner.invoke(args=["db-populate"])
    assert "populated by" in command_output.stdout

    events_query = m.Event.select().where(m.Event.date_time < datetime.now())
    events: list[m.Event] = db.session.scalars(events_query).all()
    assert events

    TESTING_TICKETS_TO_PAY_PER_EVENT = 5

    tickets_to_pay: list[m.Ticket] = []
    for event in events:
        for i in range(TESTING_TICKETS_TO_PAY_PER_EVENT):
            ticket = m.Ticket(
                seller_id=event.creator_id,
                buyer_id=random.randint(5, 10),
                event=event,
                is_sold=True,
                last_reservation_time=datetime.now() - timedelta(hours=49),
                price_net=100,
                price_gross=111,
            ).save()
            tickets_to_pay.append(ticket)
    assert tickets_to_pay
    for ticket in tickets_to_pay:
        assert ticket.is_sold
        assert ticket.last_reservation_time < datetime.now() - timedelta(hours=48)

    command_output: Result = runner.invoke(args=["pay-sellers"])
    assert f"{len(tickets_to_pay)} tickets to pay" in command_output.stdout
