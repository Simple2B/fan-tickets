from datetime import datetime
from flask import Blueprint, render_template, request, current_app as app
from flask_login import login_required
from app import schema as s, models as m, db
from app.controllers import (
    get_pagarme_customer,
    create_pagarme_customer,
    get_pagarme_card,
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
    user_unique_id = request.form.get("user_unique_id")
    username = request.form.get("username", "none")
    birthdate = request.form.get("birthdate", "01/01/2000")
    code = request.form.get("code", "00000000000")
    email = request.form.get("email", "none@email.com")
    document = request.form.get("document", "93095135270")
    phone = request.form.get("phone", "11999999999")
    number = request.form.get("card_number", 4111111111111111)
    exp_month = request.form.get("exp_month", 12)
    exp_year = request.form.get("exp_year", datetime.now().year + 1)
    cvv = request.form.get("cvv", 123)
    item_amount = request.form.get("item_amount", 0)
    item_code = request.form.get("item_code")  # ticket_unique_id
    item_description = request.form.get("item_description")
    item_quantity = request.form.get("item_quantity", 1)
    item_category = request.form.get("item_category")

    user_query = m.User.select().where(m.User.unique_id == user_unique_id)
    user: m.User = db.session.scalar(user_query)

    if user.pagarme_id:
        pagarme_customer = get_pagarme_customer(customer_id=user.pagarme_id)
    else:
        pagarme_customer = create_pagarme_customer(
            customer_name=username,
            code=code,
            email=email,
            birthdate=birthdate,
            document=document,
            phone=phone,
        )
        user.pagarme_id = pagarme_customer.id
        user.save()

    if isinstance(pagarme_customer, s.PagarmeError):
        return pagarme_customer.model_dump()

    billing_address = s.PagarmeBillingAddress(
        line_1=user.billing_line_1,
        line_2=user.billing_line_2,
        zip_code=user.billing_zip_code,
        city=user.billing_city,
        state=user.billing_state,
        country=user.billing_country,
    ).model_dump()

    if user.card_id:
        card_details = get_pagarme_card(
            customer_id=pagarme_customer.id,
            card_id=user.card_id,
        )
    else:
        card_details = create_pagarme_card(
            customer_id=pagarme_customer.id,
            holder_name=pagarme_customer.name,
            number=int(number),
            exp_month=int(exp_month),
            exp_year=int(exp_year),
            cvv=int(cvv),
            billing_address=billing_address,
        )

    card_input = s.PagarmeCardInput(
        card_id=card_details.id,
        first_six_digits=card_details.first_six_digits,
        last_four_digits=card_details.last_four_digits,
        brand=card_details.brand,
        holder_name=card_details.holder_name,
        exp_month=card_details.exp_month,
        exp_year=card_details.exp_year,
        billing_address=billing_address,
        status=card_details.status,
        type=card_details.type,
        customer=pagarme_customer,
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

    if isinstance(pagarme_customer, s.PagarmeError):
        return pagarme_customer.model_dump()

    order_create_response = create_pagarme_order(
        item_amount=int(item_amount),
        item_code=str(item_code),
        item_description=str(item_description),
        item_quantity=int(item_quantity),
        item_category=str(item_category),
        customer_id=pagarme_customer.id,
        code=pagarme_customer.code,
        payments=checkout,
    )

    return s.PagarmeCreditCardPayment(
        status=order_create_response.charges[0]["last_transaction"]["antifraud_response"]["status"],
        user_pagar_id=order_create_response.customer.code,
        ticket_unique_id=order_create_response.items[0].code,
        price_paid=order_create_response.charges[0]["last_transaction"]["amount"],
    ).model_dump()


@pay_blueprint.route("/webhook", methods=["POST"])
def webhook():
    """
    customer.created
    customer.updated
    card.created
    card.updated
    card.deleted
    card.expired
    order.paid
    order.payment_failed
    order.created
    order.canceled
    """
    with open("webhook-response.json", "w") as f:
        # f.write(request.data.decode("utf-8"))
        f.write(request.json)
    return {"status": "success"}, 200


@pay_blueprint.route("/display_response", methods=["GET", "POST"])
@login_required
def display_response():
    with open("webhook-response.json", "r") as f:
        webhook_response = f.read()
    return render_template(
        "display_response.html",
        webhook_response=webhook_response,
    )
