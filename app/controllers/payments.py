import requests
from flask import current_app as app
from app import schema as s
from app.logger import log


"""
1.  User requests my Flask app pressing for example "Pay" button
2. Flask app accepts this request at first at the route that creates a pagar.me customer going to "https://api.pagar.me/core/v5/customers" endpoint.
3. Flask app creates a pagar.me card going to the "https://api.pagar.me/core/v5/customers/customer_id/cards" endpoint.
4. Flask app creates a pagar.me order going to the "https://api.pagar.me/core/v5/orders" endpoint.
5. Flask app creates a pagar.me charge going to the "https://api.pagar.me/core/v5/charges" endpoint.
6. Flask app creates a pagar.me item going to the "https://api.pagar.me/core/v5/orders/order_id/items" endpoint.
7. Pagar.me proceeds the payment and sends a response to a flask app webhook
8. Flask app receives the response on the webhook and saves payment info to a database
"""


def get_headers():
    PAGARME_SECRET_KEY = app.config["PAGARME_SECRET_KEY"]
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {PAGARME_SECRET_KEY}",
    }
    return headers


def get_all_pagarme_customers():
    """
    Possible query parameters:
    name
    document
    email
    gender
    page
    size
    code

    Example:
    url = "https://api.pagar.me/core/v5/customers?page=1&size=10&code=10"
    """

    PAGE = 1
    SIZE = 10
    CODE = 10
    url = f"https://api.pagar.me/core/v5/customers?page={PAGE}&size={SIZE}&code={CODE}"

    response = requests.get(url, headers=get_headers())

    log(log.INFO, "get_all_pagarme_customers response: [%s]", response.text)
    return response.text


def get_pagarme_customer(customer_id: str):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}"

    response = requests.get(url, headers=get_headers())

    log(log.INFO, "get_pagarme_customer response: [%s]", response.text)
    return response.text


def create_pagarme_customer(customer_name: str, birthdate: str):
    url = "https://api.pagar.me/core/v5/customers"

    # payload = {"birthdate": "mm/dd/aaa"}
    payload = {
        "birthdate": birthdate,
        "name": customer_name,
    }

    response = requests.post(url, json=payload, headers=get_headers())

    log(log.INFO, "create_pagarme_customer response: [%s]", response.text)
    return s.PagarmeUserOutput.model_validate_json(response.text)


def update_pagarme_customer(customer_id: str, birthdate: str = None, customer_name: str = None):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}"

    payload = {}
    if birthdate:
        payload["birthdate"] = birthdate
    if customer_name:
        payload["name"] = customer_name

    response = requests.put(url, headers=get_headers(), json=payload)

    print(response.text)
    return s.PagarmeUserOutput.model_validate_json(response.text)


def create_pagarme_card(customer_id: str, holder_name: str, number: int, exp_month: int, exp_year: int, cvv: int):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards"

    payload = {
        "customer_id": customer_id,
        "holder_name": holder_name,
        "number": number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvv": cvv,
    }

    response = requests.post(url, headers=get_headers(), json=payload)

    log(log.INFO, "create_pagarme_card response: [%s]", response.text)
    return s.PagarmeCardOutput.model_validate_json(response.text)


def update_pagarme_card(customer_id: str, card_id: str):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards/{card_id}"

    response = requests.put(url, headers=get_headers())

    log(log.INFO, "update_pagarme_card response: [%s]", response.text)
    return response.text


def delete_pagarme_card(customer_id: str, card_id: str):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards/{card_id}"

    response = requests.delete(url, headers=get_headers())

    log(log.INFO, "delete_pagarme_card response: [%s]", response.text)
    return response.text


def create_pagarme_order(
    item_amount: int,
    item_description: str,
    item_quantity: int,
    item_category: str,
    customer_id: str,
    name: str,
    birthdate: str,
    payments: list[s.PagarmeCheckout],
):
    url = "https://api.pagar.me/core/v5/orders"

    payload = s.PagarmeCreateOrderInput(
        items=[
            s.PagarmeItem(
                amount=item_amount,
                description=item_description,
                quantity=item_quantity,
                category=item_category,
            ).model_dump()
        ],
        customer=s.PagarmeUserInput(
            id=customer_id,
            name=name,
            birthdate=birthdate,
        ).model_dump(),
        payments=payments,
    )

    response = requests.post(url, headers=get_headers(), json=payload)

    log(log.INFO, "create_pagarme_order response: [%s]", response.text)
    return response.text
