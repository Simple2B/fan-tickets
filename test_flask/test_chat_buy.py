from datetime import timedelta
from alchemical.flask import Alchemical
from flask.testing import FlaskClient
from flask_login import current_user
from test_flask.utils import login
from app import models as m, db, schema as s, mail_controller
from .db import populate
from app.controllers.chat_buy import get_sorted_tickets, calculate_total_price


def get_available_ticket(db: Alchemical):
    with db.session.no_autoflush:
        tickets_available: list[m.Ticket] = []
        while not tickets_available:
            populate()
            event: m.Event = db.session.scalar(m.Event.select())
            tickets: list[m.Ticket] = db.session.scalars(
                m.Ticket.select().where(
                    m.Ticket.event_id == event.id,
                    m.Ticket.is_reserved.is_(False),
                    m.Ticket.is_sold.is_(False),
                )
            ).all()
            tickets_available = [t for t in tickets if t.is_available]

    return event, tickets_available


def test_get_event_name(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)

    event, tickets_available = get_available_ticket(db)

    response = client.get(f"chat/buy/get_event_name?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "No event date provided. Please add event name" in response.data.decode()

    response = client.get(f"chat/buy/get_event_name?room_unique_id={room.unique_id}&user_message={event.name.lower()}")
    assert response.status_code == 200
    assert f"We have found {len(tickets_available)} available options" in response.data.decode()


def test_get_events_by_location(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)

    event, tickets_available = get_available_ticket(db)
    location: m.Location = db.session.scalar(m.Location.select().where(m.Location.events.any(m.Event.id == event.id)))

    response = client.get(f"/chat/buy/get_events_by_location?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Something went wrong. Please add event name" in response.data.decode()

    response = client.get(
        f"/chat/buy/get_events_by_location?room_unique_id={room.unique_id}&location_unique_id={location.unique_id}&event_name={event.name}"
    )
    assert response.status_code == 200
    assert f"We have found {len(tickets_available)} available options" in response.data.decode()

    if event.date_time:
        date_time = event.date_time + timedelta(hours=2)

    m.Event(
        name=event.name,
        date_time=date_time,
        location_id=event.location_id,
        category_id=event.category_id,
        creator_id=event.creator_id,
    ).save()

    response = client.get(
        f"/chat/buy/get_events_by_location?room_unique_id={room.unique_id}&location_unique_id={location.unique_id}&event_name={event.name}"
    )
    assert response.status_code == 200
    assert "Please, choose available options" in response.data.decode()


def test_get_tickets(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)

    event, tickets_available = get_available_ticket(db)

    response = client.get(f"/chat/buy/ticket/get_by_event?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Something went wrong. Please add event name" in response.data.decode()

    response = client.get(
        f"/chat/buy/ticket/get_by_event?room_unique_id={room.unique_id}&event_unique_id={event.unique_id}"
    )
    assert response.status_code == 200
    assert f"We have found {len(tickets_available)} available options" in response.data.decode()


def test_booking_ticket(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)

    event, tickets_available = get_available_ticket(db)

    ticket = tickets_available[0]

    response = client.get(f"/chat/buy/ticket/booking?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Would you like to be notified" in response.data.decode()

    response = client.get(
        f"/chat/buy/ticket/booking?room_unique_id={room.unique_id}&ticket_unique_id={ticket.unique_id}"
    )
    assert response.status_code == 200
    assert "To continue you need to sign in or sign up" in response.data.decode()

    login(client)
    response = client.get(
        f"/chat/buy/ticket/booking?room_unique_id={room.unique_id}&ticket_unique_id={ticket.unique_id}"
    )
    assert response.status_code == 200
    assert "Do you want to proceed to purchase?" in response.data.decode()
    assert f"{ticket.unique_id}" in response.data.decode()


def test_booking_paired_tickets(client: FlaskClient):
    from .assets.pagarme.webhook_response import WEBHOOK_RESPONSE

    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)

    _, tickets_available = get_available_ticket(db)

    ticket_1, ticket_2 = tickets_available[0:2]

    ticket_1.is_paired = True
    ticket_1.pair_unique_id = ticket_2.unique_id
    ticket_2.is_paired = True
    ticket_2.pair_unique_id = ticket_1.unique_id

    login(client)
    user: m.User = current_user
    user.buyers_service_fee = 0
    user.pagarme_id = "cus_LD8jWxauYfOm9yEe"
    response = client.get(
        f"/chat/buy/ticket/booking?room_unique_id={room.unique_id}&ticket_unique_id={ticket_1.unique_id}"
    )
    assert response.status_code == 200
    assert "Do you want to proceed to purchase?" in response.data.decode()
    assert f"{ticket_1.unique_id}" in response.data.decode()

    assert ticket_1.is_reserved
    assert ticket_1.last_reservation_time
    assert ticket_2.is_reserved
    assert ticket_2.last_reservation_time

    payment_response = client.get(
        f"/chat/buy/payment/payment?room_unique_id={room.unique_id}&ticket_unique_id={ticket_1.unique_id}"
    )
    assert payment_response.status_code == 200

    webhook_response = s.PagarmePaidWebhook.model_validate(WEBHOOK_RESPONSE)
    webhook_response.data.customer.code = current_user.uuid
    webhook_response.data.items[0].description = f"{ticket_1.unique_id}, {ticket_2.unique_id}, "

    with mail_controller.mail.record_messages() as outbox:
        response = client.post("/pay/webhook", json=webhook_response.model_dump())
        assert response.status_code == 200
        assert ticket_1.is_sold is True
        assert ticket_1.is_deleted is True
        assert ticket_1.paid_to_seller_at is None
        assert ticket_2.is_sold is True
        assert ticket_2.is_deleted is True
        assert ticket_2.paid_to_seller_at is None

        validated_response = s.FanTicketWebhookProcessed.model_validate(response.json)
        assert validated_response.status == "paid"
        assert validated_response.user_uuid == current_user.uuid
        assert validated_response.tickets_uuids_str == f"{ticket_1.unique_id}, {ticket_2.unique_id}, "

        users_payments_query = m.Payment.select().where(m.Payment.buyer_id == current_user.id)
        users_payments = db.session.scalars(users_payments_query).all()
        assert len(users_payments) == 1
        assert len(outbox) == 2

    webhook_response.data.status = "pending"
    response = client.post("/pay/webhook", json=webhook_response.model_dump())
    assert response.status_code == 200
    validated_response = s.FanTicketWebhookProcessed.model_validate(response.json)
    assert validated_response.status == "pending"


def test_get_cheapest_ticket(client_with_data: FlaskClient):
    tickets_query = m.Ticket.select().limit(5)
    tickets = db.session.scalars(tickets_query).all()

    global_settings: m.GlobalFeeSettings = db.session.scalar(m.GlobalFeeSettings.select())
    result = get_sorted_tickets(tickets, True, global_settings.tickets_sorting_by)
    assert result

    tickets = sorted(tickets, key=lambda ticket: ticket.price_net if ticket.price_net else 0)
    assert result == tickets


def test_get_most_expensive_ticket(client_with_data: FlaskClient):
    tickets_query = m.Ticket.select().limit(5)
    tickets = db.session.scalars(tickets_query).all()

    TEST_SORTING_TYPE = m.TicketsSortingType.most_expensive.value
    result = get_sorted_tickets(tickets, True, TEST_SORTING_TYPE)
    assert result

    tickets = sorted(tickets, key=lambda ticket: ticket.price_net if ticket.price_net else 0, reverse=True)
    assert result == tickets


def test_sort_tickets_by_categories(client_with_data: FlaskClient):
    # tickets_query = m.Ticket.select().where(m.Ticket.event.has(m.Event.location.has(m.Location.name == "São Paulo")))
    tickets_query = m.Ticket.select().limit(30)
    tickets = db.session.scalars(tickets_query).all()
    categories = set(ticket.event.category.name for ticket in tickets)

    TEST_SORTING_TYPE = m.TicketsSortingType.category.value
    result = get_sorted_tickets(tickets, True, TEST_SORTING_TYPE)
    assert len(result) == len(categories)


def test_fee_adjustment(client: FlaskClient):
    login(client)
    user: m.User = current_user
    user.buyers_service_fee = 0
    user.buyers_bank_fee = 0

    _, tickets_available = get_available_ticket(db)

    ticket = tickets_available[0]
    ticket.is_reserved = True
    ticket.buyer_id = user.id
    ticket.seller.sellers_service_fee = 0
    ticket.seller.sellers_bank_fee = 0
    ticket.save()
    result = calculate_total_price(user)
    assert result
    assert result.total == ticket.price_net
