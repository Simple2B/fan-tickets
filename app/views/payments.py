import io
from datetime import datetime
import sqlalchemy as sa
from flask import render_template, Blueprint, request, abort, send_file
from flask_login import login_required, current_user

from app.logger import log
from app import schema as s, models as m, db
from app import pagarme_client, mail_controller
from app import forms as f
from app.controllers import get_room, utcnow_chat_format

pay_blueprint = Blueprint("pay", __name__, url_prefix="/pay")


@pay_blueprint.route("/ticket_order", methods=["GET", "POST"])
@login_required
def ticket_order():
    cu: m.User = current_user
    payment_method = request.args.get("payment_method", "pix")

    if not cu.phone:
        return render_template(
            "chat/chat_error.html",
            error_message="You did not add your phone",
            now=utcnow_chat_format(),
        )

    if payment_method == "pix":
        card_form = f.OrderForm()
    elif payment_method == "credit_card":
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
            "chat/buy/payment.html",
            error_message=f"Form submitting error: {card_form.errors}",
            room=room,
            now=utcnow_chat_format(),
            form=card_form,
        )

    user_query = m.User.select().where(m.User.uuid == cu.uuid)
    user: m.User = db.session.scalar(user_query)

    tickets = db.session.scalars(
        sa.select(m.Ticket).where(
            m.Ticket.buyer_id == cu.id,
            m.Ticket.is_reserved.is_(True),
            m.Ticket.is_sold.is_(False),
        )
    ).all()

    if user.pagarme_id:
        pagarme_customer = pagarme_client.get_customer(user.pagarme_id)
    else:
        # TODO: remove hard code phone number
        phone_data = pagarme_client.generate_customer_phone("432337789")
        phones_data = s.PagarmeCustomerPhones(
            mobile_phone=phone_data,
        )

        customer_data = s.PagarmeCustomerCreate(
            name=cu.username,
            birthdate="03/13/1990",
            code=cu.unique_id,
            email=cu.email,
            document=card_form.document_identity_number.data,
            phones=phones_data,
        )

        pagarme_customer = pagarme_client.create_customer(customer_data)

        assert pagarme_customer

        user.pagarme_id = pagarme_customer.id
        user.save()

    billing_address = s.PagarmeBillingAddress(
        line_1="Avenue7",
        line_2=user.billing_line_2,
        zip_code="02332132",
        city="Rio de Janeiro",
        state="RJ",
        country="BR",
    )

    assert pagarme_customer

    if payment_method == "credit_card":
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
                # TODO: change price to int
                amount=int(ticket.price_gross) * 100,
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

    response = s.PagarmeCreditCardPayment(
        status=order_create_response.charges[0]["last_transaction"]["status"],
        user_pagar_id=order_create_response.customer.code,
        ticket_unique_id=order_create_response.items[0].code,
        price_paid=order_create_response.charges[0]["last_transaction"]["amount"],
    ).model_dump()

    if response["status"] == "captured":
        for ticket in tickets:
            ticket.is_reserved = False
            ticket.is_sold = True

        db.session.commit()

        log(log.INFO, "Payment success: [%s]", response)
        return render_template(
            "chat/buy/payment_success.html",
            room=room,
            tickets=tickets,
            now=utcnow_chat_format(),
        )

    log(log.ERROR, "Payment error: [%s]", response)
    return render_template(
        "chat/buy/payment.html",
        error_message="Something went wrong, try again please",
        room=room,
        now=utcnow_chat_format(),
    )


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

    log(log.INFO, "Webhook received: [%s]", request.json)
    webhook_request = s.PagarmePaidWebhook.model_validate(request.json)
    request_data = webhook_request.data
    status = request_data.status if request_data else None
    if status:
        log(log.INFO, "Webhook status: [%s]", status)

    buyer_uuid = None
    tickets_uuids_str = None
    tickets = []
    if status and status == "paid":
        buyer_uuid = request_data.customer.code
        buyer_query = m.User.select().where(m.User.uuid == buyer_uuid)
        buyer: m.User = db.session.scalar(buyer_query)
        log(log.INFO, "User: [%s]", buyer)

        tickets_uuids_str = request_data.items[0].description
        tickets_uuids = tickets_uuids_str.split(", ")
        log(log.INFO, "Tickets uuids: [%s]", tickets_uuids)

        for i, ticket_uuid in enumerate(tickets_uuids):
            if ticket_uuid:
                ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_uuid)
                ticket: m.Ticket = db.session.scalar(ticket_query)
                ticket.is_sold = True
                ticket.is_deleted = True
                if ticket.file:
                    ticket.is_transferred = True
                    email_message_to_buyer = "The ticket is in PDF format. Please download it in your profile."
                    email_message_to_seller = "Ticket's PDF file is available to download for the buyer."
                    log(log.INFO, "Ticket's PDF file is available to download")
                else:
                    email_message_to_buyer = (
                        "The ticket is in wallet id format. Please confirm the transfer in your profile."
                    )
                    email_message_to_seller = f"Please transfer the ticket {ticket.wallet_id} to the buyer's wallet."
                    log(log.INFO, "Ticket's wallet_id: [%s]", ticket.wallet_id)
                ticket.save()

                if ticket.is_paired:
                    description = f"Tickets: {ticket.unique_id}, {ticket.pair_unique_id}. Buyer: {buyer}"
                else:
                    description = f"Ticket {ticket.unique_id}. Buyer: {buyer}"

                if i == 0:
                    m.Payment(
                        buyer=buyer,
                        ticket=ticket,
                        description=description,
                    ).save()

                    mail_controller.send_email(
                        [buyer],
                        "Ticket transfer",
                        render_template(
                            "email/ticket_transfer.htm",
                            event_name=ticket.event.name,
                            date_time=ticket.event.date_time.strftime("%Y-%m-%d %H:%M")
                            if ticket.event.date_time
                            else "",
                            ticket_id=str(ticket.id).zfill(8),
                            message=email_message_to_buyer,
                        ),
                    )

                    mail_controller.send_email(
                        [ticket.seller],
                        "Ticket transfer",
                        render_template(
                            "email/ticket_transfer.htm",
                            event_name=ticket.event.name,
                            date_time=ticket.event.date_time.strftime("%Y-%m-%d %H:%M")
                            if ticket.event.date_time
                            else "",
                            ticket_id=str(ticket.id).zfill(8),
                            message=email_message_to_seller,
                        ),
                    )

                # TODO: add a notification instance
                ticket_data = s.FanTicketWebhookTicketData(
                    unique_id=ticket.unique_id,
                    is_paired=ticket.is_paired,
                    pair_unique_id=ticket.pair_unique_id,
                    is_reserved=ticket.is_reserved,
                    is_sold=ticket.is_sold,
                    is_deleted=ticket.is_deleted,
                )
                tickets.append(ticket_data)
                log(log.INFO, "Ticket sold: [%s]", ticket_uuid)

    return s.FanTicketWebhookProcessed(
        status=status,
        user_uuid=buyer_uuid,
        tickets_uuids_str=tickets_uuids_str,
        tickets=tickets,
    ).model_dump()


@pay_blueprint.route("/transfer")
@login_required
def transfer():
    """
    Transfer ticket to another user
    """
    ticket_unique_id = request.args.get("ticket_unique_id")
    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    if not ticket:
        abort(404)

    if ticket.buyer_id != current_user.id:
        abort(403)

    if ticket.is_transferred:
        ticket.is_transferred = False
    else:
        ticket.is_transferred = True
    if ticket.is_paired:
        paired_ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket.pair_unique_id)
        paired_ticket: m.Ticket = db.session.scalar(paired_ticket_query)
        if paired_ticket.is_transferred:
            paired_ticket.is_transferred = False
        else:
            paired_ticket.is_transferred = True
        paired_ticket.save(False)
    ticket.save()

    payments_query = m.Payment.select().where(m.Payment.buyer_id == ticket.buyer.id)
    payments = db.session.scalars(payments_query).all()

    if not payments:
        log(log.ERROR, "Payments not found")
        abort(404)

    return render_template("user/ticket_transfer.html", payments=payments)


@pay_blueprint.route("/download_pdf")
@login_required
def download_pdf():
    ticket_unique_id = request.args.get("ticket_unique_id")
    ticket_query = m.Ticket.select().where(m.Ticket.unique_id == ticket_unique_id)
    ticket: m.Ticket = db.session.scalar(ticket_query)

    if not ticket:
        abort(404)

    if ticket.buyer_id != current_user.id:
        abort(403)

    if not ticket.file:
        log(log.ERROR, "Ticket's PDF file not found")
        abort(404)

    now = datetime.now()
    return send_file(
        io.BytesIO(ticket.file),
        as_attachment=True,
        download_name=f"fan_ticket_users_{now.strftime('%Y-%m-%d-%H-%M-%S')}.pdf",
        mimetype="application/pdf",
        max_age=0,
        last_modified=now,
    )
