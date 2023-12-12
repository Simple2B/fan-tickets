from flask import current_app as app
from flask.testing import FlaskClient
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

    room: m.Room = m.Room.first()
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

    response = client.get(f"/buy/event_tickets?event_unique_id={event.unique_id}&room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Subscribe" in response.data.decode()
    assert "Another events" in response.data.decode()
    tickets_number = len(event.tickets)
    assert f"loop.index: {tickets_number}" in response.data.decode()
