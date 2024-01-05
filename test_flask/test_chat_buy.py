from datetime import timedelta
from flask.testing import FlaskClient
from test_flask.utils import login
from app import models as m, db
from .db import populate


def test_get_event_name(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    populate()
    event: m.Event = db.session.scalar(m.Event.select())
    event_name = event.name[:1]
    events = db.session.scalars(m.Event.select().where(m.Event.name.ilike(f"%{event_name}%"))).all()
    locations_query = m.Location.select().filter(
        m.Location.event.has(m.Event.name.in_([event.name for event in events]))
    )
    locations: list[m.Location] = db.session.scalars(locations_query).all()
    tickets: list[m.Ticket] = db.session.scalars(
        m.Ticket.select().where(
            m.Ticket.event_id == event.id,
            m.Ticket.is_reserved.is_(False),
            m.Ticket.is_sold.is_(False),
        )
    ).all()

    response = client.get(f"/buy/get_event_name?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "No event date provided. Please add event name" in response.data.decode()

    response = client.get(f"/buy/get_event_name?room_unique_id={room.unique_id}&user_message={event_name.lower()}")
    assert response.status_code == 200
    assert f"locations length {len(locations)}" in response.data.decode()

    response = client.get(f"/buy/get_event_name?room_unique_id={room.unique_id}&user_message={event.name.lower()}")
    assert response.status_code == 200
    assert f"We have found {len(tickets)} available tickets" in response.data.decode()


def test_get_events_by_location(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    populate()
    event: m.Event = db.session.scalar(m.Event.select())
    location: m.Location = db.session.scalar(m.Location.select().where(m.Location.event == event))
    tickets: list[m.Ticket] = db.session.scalars(
        m.Ticket.select().where(
            m.Ticket.event_id == event.id,
            m.Ticket.is_reserved.is_(False),
            m.Ticket.is_sold.is_(False),
        )
    ).all()

    response = client.get(f"/buy/get_events_by_location?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Something went wrong. Please add event name" in response.data.decode()

    response = client.get(
        f"/buy/get_events_by_location?room_unique_id={room.unique_id}&location_unique_id={location.unique_id}&event_name={event.name}"
    )
    assert response.status_code == 200
    assert f"We have found {len(tickets)} available tickets" in response.data.decode()

    m.Event(
        name=event.name,
        date_time=event.date_time + timedelta(hours=2),
        location_id=event.location_id,
        category_id=event.category_id,
        creator_id=event.creator_id,
    ).save()

    response = client.get(
        f"/buy/get_events_by_location?room_unique_id={room.unique_id}&location_unique_id={location.unique_id}&event_name={event.name}"
    )
    assert response.status_code == 200
    assert "Please specify the date and time" in response.data.decode()


def test_get_tickets(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    populate()
    event: m.Event = db.session.scalar(m.Event.select())
    tickets: list[m.Ticket] = db.session.scalars(
        m.Ticket.select().where(
            m.Ticket.event_id == event.id,
            m.Ticket.is_reserved.is_(False),
            m.Ticket.is_sold.is_(False),
        )
    ).all()

    response = client.get(f"/buy/get_tickets?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Something went wrong. Please add event name" in response.data.decode()

    response = client.get(f"/buy/get_tickets?room_unique_id={room.unique_id}&event_unique_id={event.unique_id}")
    assert response.status_code == 200
    assert f"We have found {len(tickets)} available tickets" in response.data.decode()


def test_booking_ticket(client: FlaskClient):
    room = m.Room(
        seller_id=None,
        buyer_id=2,
    ).save(False)
    populate()
    event: m.Event = db.session.scalar(m.Event.select())
    ticket: m.Ticket = db.session.scalar(
        m.Ticket.select().where(
            m.Ticket.event_id == event.id,
            m.Ticket.is_reserved.is_(False),
            m.Ticket.is_sold.is_(False),
        )
    )

    response = client.get(f"/buy/booking_ticket?room_unique_id={room.unique_id}")
    assert response.status_code == 200
    assert "Would you like to be notified" in response.data.decode()

    response = client.get(f"/buy/booking_ticket?room_unique_id={room.unique_id}&ticket_unique_id={ticket.unique_id}")
    assert response.status_code == 200
    assert "To continue you need to sign in or sign up" in response.data.decode()

    login(client)
    response = client.get(f"/buy/booking_ticket?room_unique_id={room.unique_id}&ticket_unique_id={ticket.unique_id}")
    assert response.status_code == 200
    assert "Do you want to buy another one or proceed to purchase?" in response.data.decode()
    assert f"{ticket.unique_id}" in response.data.decode()
