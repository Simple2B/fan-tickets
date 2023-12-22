from datetime import datetime
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
    code = request.form.get("code")
    email = request.form.get("email")
    document = request.form.get("document")
    phone = request.form.get("phone")
    number = request.form.get("card_number")
    exp_month = request.form.get("exp_month")
    exp_year = request.form.get("exp_year")
    cvv = request.form.get("cvv")
    billing_line_1 = request.form.get("billing_line_1")
    billing_line_2 = request.form.get("billing_line_2")
    billing_zip_code = request.form.get("billing_zip_code")
    billing_city = request.form.get("billing_city")
    billing_state = request.form.get("billing_state")
    billing_country = request.form.get("billing_country")
    item_amount = request.form.get("item_amount")
    item_code = request.form.get("item_code")
    item_description = request.form.get("item_description")
    item_quantity = request.form.get("item_quantity")
    item_category = request.form.get("item_category")

    created_pagarme_customer = create_pagarme_customer(
        customer_name=username,
        code=code,
        email=email,
        birthdate=birthdate,
        document=document,
        phone=phone,
    )

    billing_address = s.PagarmeBillingAddress(
        line_1=billing_line_1,
        line_2=billing_line_2,
        zip_code=billing_zip_code,
        city=billing_city,
        state=billing_state,
        country=billing_country,
    ).model_dump()

    card_create_response = create_pagarme_card(
        customer_id=created_pagarme_customer.id,
        holder_name=created_pagarme_customer.name,
        number=number,
        exp_month=exp_month,
        exp_year=exp_year,
        cvv=cvv,
        billing_address=billing_address,
    )

    card_input = s.PagarmeCardInput(
        card_id=card_create_response.id,
        first_six_digits=card_create_response.first_six_digits,
        last_four_digits=card_create_response.last_four_digits,
        brand=card_create_response.brand,
        holder_name=card_create_response.holder_name,
        exp_month=card_create_response.exp_month,
        exp_year=card_create_response.exp_year,
        billing_address=billing_address,
        status=card_create_response.status,
        type=card_create_response.type,
        customer=created_pagarme_customer,
    )

    checkout = [
        s.PagarmeCheckout(
            expires_in=app.config["PAGARME_CHECKOUT_EXPIRES_IN"],
            payment_method=app.config["PAGARME_DEFAULT_PAYMENT_METHOD"],
            billing_address_editable=False,
            customer_editable=False,
            accepted_payment_methods=[app.config["PAGARME_DEFAULT_PAYMENT_METHOD"]],
            success_url=f"{app.config['STAGING_BASE_URL']}/pay/webhook",
            credit_card=card_input,
        ).model_dump()
    ]

    birthdate_dt = datetime.fromisoformat(created_pagarme_customer.birthdate)
    birthdate_str = birthdate_dt.strftime("%d/%m/%Y")

    order_create_response = create_pagarme_order(
        item_amount=item_amount,
        item_code=item_code,
        item_description=item_description,
        item_quantity=item_quantity,
        item_category=item_category,
        customer_id=created_pagarme_customer.id,
        code=created_pagarme_customer.code,
        name=created_pagarme_customer.name,
        birthdate=birthdate_str,
        payments=checkout,
    )

    checkout_url = order_create_response.checkout_url

    return {
        "status": "success",
        "username": created_pagarme_customer.name,
        "birthdate": created_pagarme_customer.birthdate,
        "checkout_url": checkout_url,
    }, 200


@pay_blueprint.route("/webhook", methods=["POST"])
def webhook():
    return {"status": "success"}, 200
