from flask import Blueprint, request, current_app as app
from flask_login import login_required
from app import schema as s
from app.controllers import (
    create_pagarme_customer,
    create_pagarme_card,
    create_pagarme_order,
)

pay_blueprint = Blueprint("pay", __name__, url_prefix="/pay")


"""
1.  User requests my web app pressing for example "Pay" button
2. Web app accepts this request at first at the route that creates a pagar.me customer going to "https://api.pagar.me/core/v5/customers" endpoint.
3. Web app creates a pagar.me card going to the "https://api.pagar.me/core/v5/customers/customer_id/cards" endpoint.
4. Web app creates a pagar.me order going to the "https://api.pagar.me/core/v5/orders" endpoint.
5. Web app creates a pagar.me charge going to the "https://api.pagar.me/core/v5/charges" endpoint.
6. Web app creates a pagar.me item going to the "https://api.pagar.me/core/v5/orders/order_id/items" endpoint.
7. Pagar.me proceeds the payment and sends a response to a web app webhook
8. Web app receives the response on the webhook and saves payment info to a database
"""


@pay_blueprint.route("/ticket_order", methods=["GET", "POST"])
@login_required
def ticket_order():
    username = request.form.get("username")
    birthdate = request.form.get("birthdate")
    number = request.form.get("number")
    exp_month = request.form.get("exp_month")
    exp_year = request.form.get("exp_year")
    cvv = request.form.get("cvv")
    item_amount = request.form.get("item_amount")
    item_description = request.form.get("item_description")
    item_quantity = request.form.get("item_quantity")
    item_category = request.form.get("item_category")
    customer_id = request.form.get("customer_id")
    name = request.form.get("name")
    created_at = request.form.get("created_at")
    updated_at = request.form.get("updated_at")
    payments = request.form.get("payments")

    created_pagarme_customer = create_pagarme_customer(username, birthdate)

    card_create_response = create_pagarme_card(
        customer_id=created_pagarme_customer.id,
        holder_name=created_pagarme_customer.name,
        number=number,
        exp_month=exp_month,
        exp_year=exp_year,
        cvv=cvv,
    )

    checkout = [
        s.PagarmeCheckout(
            expires_in=app.config["PAGARME_CHECKOUT_EXPIRES_IN"],
            default_payment_method=app.config["PAGARME_DEFAULT_PAYMENT_METHOD"],
            billing_address_editable=False,
            customer_editable=False,
            accepted_payment_methods=[app.config["PAGARME_DEFAULT_PAYMENT_METHOD"]],
            success_url=f"{app.config['STAGING_BASE_URL']}/pay/webhook",
            credit_card=card_create_response,
        )
    ]

    order_create_response = create_pagarme_order(
        ...,
    )

    return {
        "status": "success",
        "username": created_pagarme_customer.name,
        "birthdate": created_pagarme_customer.birthdate,
    }, 200


@pay_blueprint.route("/webhook", methods=["POST"])
def webhook():
    return {"status": "success"}, 200
