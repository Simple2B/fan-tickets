from typing import Any
from flask import current_app as app
from flask.testing import FlaskClient
from test_flask.utils import login
from app import models as m, db
from .db import populate


def test_chat_buy_get_events(client: FlaskClient):
    response = client.get("/buy/")
    assert response.status_code == 200
    assert b"No event location provided" in response.data

    populate()
    event: m.Event = db.session.scalar(m.Event.select())
    date_str = event.date_time.strftime(app.config["DATE_PICKER_FORMAT"])
    response = client.get(f"/buy/?event_location={event.location.name}&event_date={date_str}")
    assert response.status_code == 200
    assert b"Choose an event from the list." in response.data
    assert event.name in response.data.decode()

    room: m.Room | Any = m.Room.first()
    response = client.get(f"/buy/event?event_unique_id={event.unique_id}&room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert event.name in response.data.decode()
    assert event.location.name in response.data.decode()

    response = client.get(f"/buy/event?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert b"Event not found" in response.data

    response = client.get(f"/buy/event?event_unique_id={event.unique_id}")
    assert response.status_code == 200
    assert b"Form submitting error" in response.data


def test_chat_buy_get_event_tickets(client_with_data: FlaskClient):
    event: m.Event = db.session.scalar(m.Event.select())
    room = m.Room(
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    response = client_with_data.get(
        f"/buy/event_tickets?event_unique_id={event.unique_id}&room_unique_id={room.unique_id}"
    )
    assert response.status_code == 200
    assert "Subscribe" in response.data.decode()
    assert "Another events" in response.data.decode()
    tickets_number = len(event.tickets)
    assert f"loop.index: {tickets_number}" in response.data.decode()


def test_chat_buy_ticket_details(client_with_data: FlaskClient):
    room = m.Room(
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    event: m.Event = db.session.scalar(m.Event.select())
    ticket = event.tickets[0]
    response = client_with_data.get(
        f"/buy/ticket_details?event_unique_id={event.unique_id}&room_unique_id={room.unique_id}&ticket_unique_id={ticket.unique_id}"
    )
    assert response.status_code == 200
    assert "Buy" in response.data.decode()
    assert "Reserve" in response.data.decode()
    assert "Back" in response.data.decode()
    assert f"Section: {ticket.section}" in response.data.decode()
    assert f"Queue: {ticket.queue}" in response.data.decode()
    assert f"Seat: {ticket.seat}" in response.data.decode()


def test_chat_cart(client_with_data: FlaskClient):
    response = client_with_data.get("/buy/cart")
    assert response.status_code == 302

    room = m.Room(
        seller_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    event: m.Event = db.session.scalar(m.Event.select())
    login(client_with_data)
    response = client_with_data.get(f"/buy/cart?room_unique_id={room.unique_id}&event_unique_id={event.unique_id}")
    assert response.status_code == 200
    assert "Ticket not found" in response.data.decode()

    ticket = event.tickets[0]
    room = m.Room(
        seller_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    response = client_with_data.get(
        f"/buy/cart?room_unique_id={room.unique_id}&event_unique_id={event.unique_id}&ticket_unique_id={ticket.unique_id}"
    )
    assert response.status_code == 200
    assert f"Section: {ticket.section}" in response.data.decode()
    assert f"Queue: {ticket.queue}" in response.data.decode()
    assert f"Seat: {ticket.seat}" in response.data.decode()
    assert "Total price:" in response.data.decode()
