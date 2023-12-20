import requests
from flask import current_app as app
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

PAGARME_SECRET_KEY = app.config["PAGARME_SECRET_KEY"]
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Basic {PAGARME_SECRET_KEY}",
}


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

    response = requests.get(url, headers=headers)

    log(log.INFO, "get_all_pagarme_customers response: [%s]", response.text)
    return response.text


def get_pagarme_customer(customer_id: str):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}"

    response = requests.get(url, headers=headers)

    log(log.INFO, "get_pagarme_customer response: [%s]", response.text)
    return response.text


def create_pagarme_customer(birthdate: str):
    url = "https://api.pagar.me/core/v5/customers"

    # payload = {"birthdate": "mm/dd/aaa"}
    payload = {"birthdate": birthdate}

    response = requests.post(url, json=payload, headers=headers)

    log(log.INFO, "create_pagarme_customer response: [%s]", response.text)
    return response.text


def update_pagarme_customer(customer_id: str):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}"

    response = requests.put(url, headers=headers)

    print(response.text)
    return response.text


def create_pagarme_card(customer_id: str):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards"

    response = requests.post(url, headers=headers)

    log(log.INFO, "create_pagarme_card response: [%s]", response.text)
    return response.text


def update_pagarme_card(customer_id: str, card_id: str):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards/{card_id}"

    response = requests.put(url, headers=headers)

    log(log.INFO, "update_pagarme_card response: [%s]", response.text)
    return response.text


def delete_pagarme_card(customer_id: str, card_id: str):
    url = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards/{card_id}"

    response = requests.delete(url, headers=headers)

    log(log.INFO, "delete_pagarme_card response: [%s]", response.text)
    return response.text


def create_pagarme_order():
    url = "https://api.pagar.me/core/v5/orders"

    response = requests.post(url, headers=headers)

    log(log.INFO, "create_pagarme_order response: [%s]", response.text)
    return response.text


def create_pagarme_charge():
    url = "https://api.pagar.me/core/v5/orders"

    response = requests.post(url, headers=headers)

    log(log.INFO, "create_pagarme_charge response: [%s]", response.text)
    return response.text


def create_pagarme_item():
    url = "https://api.pagar.me/core/v5/orders"

    response = requests.post(url, headers=headers)

    log(log.INFO, "create_pagarme_item response: [%s]", response.text)
    return response.text
