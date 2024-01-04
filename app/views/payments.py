import sqlalchemy as sa

from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app.logger import log
from app import schema as s, models as m, db
from app import pagarme_client
from app import forms as f
from app.controllers import (
    get_pagarme_customer,
    create_pagarme_customer,
    get_pagarme_card,
    create_pagarme_card,
    create_pagarme_order,
    get_room,
    utcnow_chat_format,
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
    current_user: m.User = current_user

    if not current_user.phone:
        return render_template(
            "chat/chat_error.html",
            error_message="You did not add your phone",
            now=utcnow_chat_format(),
        )

    card_form = f.OrderCreateForm()
    room = get_room(card_form.room_unique_id.data)

    if not room:
        return render_template(
            "chat/chat_error.html",
            error_message="Form submitting error",
            now=utcnow_chat_format(),
        )

    if not card_form.validate_on_submit():
        log(
            log.ERROR,
            "Form submitting error: [%s]",
            card_form.errors,
        )
        return render_template(
            "chat/registration/password.html",
            error_message="You did not add your password",
            room=room,
            now=utcnow_chat_format(),
            user_unique_id=card_form.user_unique_id.data,
            form=card_form,
        )

    user_query = m.User.select().where(m.User.unique_id == current_user.unique_id)
    user: m.User = db.session.scalar(user_query)

    tickets = db.session.scalars(
        sa.select(m.Ticket).where(m.Ticket.buyer_id == current_user.id, m.Ticket.is_reserved.is_(True))
    )

    if user.pagarme_id:
        pagarme_client.get_customer(user.pagarme_id)
    else:
        phone_data = pagarme_client.generate_customer_phone(current_user.phone)
        phones_data = s.PagarmeCustomerPhones(
            mobile_phone=phone_data,
        )

        customer_data = s.PagarmeCustomerCreate(
            name=current_user.username,
            birthdate=current_user.birth_date,
            code=current_user.pagarme_id,
            email=current_user.email,
            document=card_form.document_identity_number.data,
            phones=phones_data,
        )

        pagarme_customer = pagarme_client.create_customer(customer_data)

        user.pagarme_id = pagarme_customer.id
        user.save()

    billing_address = s.PagarmeBillingAddress(
        line_1=user.billing_line_1,
        line_2=user.billing_line_2,
        zip_code=user.billing_zip_code,
        city=user.billing_city,
        state=user.billing_state,
        country=user.billing_country,
    )

    if user.card_id:
        card_details = pagarme_client.get_customer_card(
            customer_id=pagarme_customer.id,
            card_id=user.card_id,
        )
    else:
        card_data = s.PagarmeCardCreate(
            customer_id=pagarme_customer.id,
            holder_name=pagarme_customer.name,
            number=card_form.card_number.data,
            exp_month=card_form.exp_month.data,
            exp_year=card_form.exp_year.data,
            cvv=card_form.cvv.data,
            billing_address=billing_address,
        )

        card_details = pagarme_client.create_customer_card(card_data)

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
        pagarme_client.generate_checkout_data(card_input),
    ]

    order_items = []
    for ticket in tickets:
        order_items.append(
            s.PagarmeItem(
                amount=ticket.price_gross,
                code=ticket.unique_id,
                description="Ticket",
                quantity=1,
                # TODO investigate: category=int(item_category),
            )
        )

    order_data = s.PagarmeCreateOrderInput(
        items=order_items,
        code=pagarme_customer.code,
        customer_id=pagarme_customer.id,
        payments=checkout,
    )

    order_create_response = pagarme_client.create_order(order_data)

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
    return {"status": "success"}, 200
