import requests
import json
from app import schema as s
from app.logger import log
from config import config


"""
1. User requests my Flask app pressing for example "Pay" button
2. Checking if we have this customer on pagar.me https://api.pagar.me/core/v5/customers/{customer_id}
3. If not creating a pagar.me customer going to "https://api.pagar.me/core/v5/customers" endpoint.
4. For new user creating a pagar.me card going to the "https://api.pagar.me/core/v5/customers/customer_id/cards" endpoint.
5. Creating a pagar.me order going to the "https://api.pagar.me/core/v5/orders" endpoint.
6. Receiving a request from pagar.me to the webhook and saving/updating all user data to the database.
"""


CFG = config()
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Basic {CFG.PAGARME_SECRET_KEY}",
}


def get_all_pagarme_customers():
    URL = "https://api.pagar.me/core/v5/customers"

    response = requests.get(URL, headers=HEADERS)

    log(log.INFO, "get_all_pagarme_customers response: [%s]", response.text)
    return response.json()


def get_pagarme_customer(customer_id: str) -> s.PagarmeCustomerOutput | s.PagarmeError:
    URL = f"https://api.pagar.me/core/v5/customers/{customer_id}"

    response = requests.get(URL, headers=HEADERS)

    log(log.INFO, "get_pagarme_customer response: [%s]", response.text)
    if "Customer not found" in response.text:
        return s.PagarmeError(
            status_code=404,
            error="Customer not found",
        )
    return s.PagarmeCustomerOutput.model_validate(response.json())


def create_pagarme_customer(
    customer_name: str,
    code: str,
    email: str,
    birthdate: str,
    document: str,
    phone: str,
) -> s.PagarmeCustomerOutput:
    URL = "https://api.pagar.me/core/v5/customers"

    """
    payload = {
        "name": customer_name,
        "birthdate": birthdate,
        "code": code,
        "email": email,
        "document": document,
        "type": "individual",
        "phones": {
            "mobile_phone": {
                "country_code": CFG.BRASIL_COUNTRY_PHONE_CODE,
                "area_code": CFG.BRASIL_COUNTRY_AREA_CODE,
                "number": phone,
            },
        },
    }
    """
    payload = s.PagarmeCustomerCreate(
        name=customer_name,
        birthdate=birthdate,
        code=code,
        email=email,
        document=document,
        phones=s.PagarmeCustomerPhones(
            mobile_phone=s.PagarmeCustomerMobilePhone(
                country_code=CFG.BRASIL_COUNTRY_PHONE_CODE,
                area_code=CFG.BRASIL_COUNTRY_AREA_CODE,
                number=phone,
            )
        ),
    ).model_dump()

    response = requests.post(URL, json=payload, headers=HEADERS)

    log(log.INFO, "create_pagarme_customer response: [%s]", response.text)
    return s.PagarmeCustomerOutput.model_validate(response.json())


def update_pagarme_customer(
    customer_id: str,
    birthdate: str | None = None,
    customer_name: str | None = None,
) -> s.PagarmeCustomerOutput:
    URL = f"https://api.pagar.me/core/v5/customers/{customer_id}"

    payload = {}
    if birthdate:
        payload["birthdate"] = birthdate
    if customer_name:
        payload["name"] = customer_name

    response = requests.put(URL, headers=HEADERS, json=payload)

    print(response.text)
    return s.PagarmeCustomerOutput.model_validate(response.json())


def create_pagarme_card(
    customer_id: str,
    holder_name: str,
    number: int,
    exp_month: int,
    exp_year: int,
    cvv: int,
    billing_address: dict,
) -> s.PagarmeCardOutput | s.PagarmeError:
    URL = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards"

    """
    payload = {
        "customer_id": customer_id,
        "holder_name": holder_name,
        "number": number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvv": cvv,
        "billing_address": billing_address,
    }
    """
    payload = s.PagarmeCardCreate(
        customer_id=customer_id,
        holder_name=holder_name,
        number=number,
        exp_month=exp_month,
        exp_year=exp_year,
        cvv=cvv,
        billing_address=billing_address,
    ).model_dump()

    response = requests.post(URL, headers=HEADERS, json=payload)

    log(log.INFO, "create_pagarme_card response: [%s]", response.text)
    if "error" in response.text:
        return s.PagarmeError(
            status_code=404,
            error="Card not found",
        )
    return s.PagarmeCardOutput.model_validate(response.json())


def get_pagarme_card(customer_id: str, card_id: str):
    URL = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards/{card_id}"

    response = requests.get(URL, headers=HEADERS)

    log(log.INFO, "get_pagarme_cards response: [%s]", response.text)
    return s.PagarmeCardOutput.model_validate(response.json())


def update_pagarme_card(customer_id: str, card_id: str):
    URL = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards/{card_id}"

    response = requests.put(URL, headers=HEADERS)

    log(log.INFO, "update_pagarme_card response: [%s]", response.text)
    return response.text


def delete_pagarme_card(customer_id: str, card_id: str):
    URL = f"https://api.pagar.me/core/v5/customers/{customer_id}/cards/{card_id}"

    response = requests.delete(URL, headers=HEADERS)

    log(log.INFO, "delete_pagarme_card response: [%s]", response.text)
    return response.text


def create_pagarme_order(
    item_amount: int,
    item_code: str,
    item_description: str,
    item_quantity: int,
    item_category: str,
    customer_id: str,
    code: str,
    payments: list[dict],
):
    URL = "https://api.pagar.me/core/v5/orders"

    payload = s.PagarmeCreateOrderInput(
        items=[
            s.PagarmeItem(
                amount=item_amount,
                code=item_code,
                description=item_description,
                quantity=item_quantity,
                category=item_category,
            ).model_dump()
        ],
        code=code,
        customer_id=customer_id,
        payments=payments,
    ).model_dump()

    with open("order-request.json", "w") as f:
        f.write(json.dumps(payload))

    response = requests.post(URL, headers=HEADERS, json=payload)

    with open("order-response.json", "w") as f:
        f.write(response.text)

    log(log.INFO, "create_pagarme_order response: [%s]", response.text)
    return s.PagarmeCreateOrderOutput.model_validate(response.json())
