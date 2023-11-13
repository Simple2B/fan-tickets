from datetime import timedelta
from .db import populate, generate_test_users, generate_test_events
from app import db
from app import models as m


TESTING_USERS_NUMBER = 30


def test_generate_users(client):
    generate_test_users(TESTING_USERS_NUMBER)
    users_list = list(db.session.scalars(m.User.select()).all())
    assert len(users_list) == TESTING_USERS_NUMBER + 1
    admins_query = m.User.select().where(m.User.role == m.UserRole.admin.value)
    admins = list(db.session.scalars(admins_query))
    assert len(admins) == 3


def test_generate_events(client):
    generate_test_events()
    locations_query = m.Location.select()
    locations = list(db.session.scalars(locations_query))
    assert len(locations) == 6
    events_query = m.Event.select()
    events = list(db.session.scalars(events_query))
    assert len(events) == 12
    tickets_query = m.Ticket.select()
    tickets = list(db.session.scalars(tickets_query))
    assert len(tickets) == 144
    disputes_query = m.Dispute.select()
    disputes = list(db.session.scalars(disputes_query))
    assert len(disputes) == 144
    room_query = m.Room.select()
    rooms = list(db.session.scalars(room_query))
    assert len(rooms) == 576
    messages_query = m.Message.select()
    messages = list(db.session.scalars(messages_query))
    assert len(messages) == 576 * 5


def test_get_events(client):
    populate(23)
    TEST_USER_ID = 12
    testing_event = db.session.scalar(m.Event.select())
    test_location_name = testing_event.location.name
    date_from = (testing_event.date_time - timedelta(days=3)).isoformat()
    date_to = (testing_event.date_time + timedelta(days=3)).isoformat()
    payload = {
        "user_id": TEST_USER_ID,
        "token": "testing_whatsapp_token",
        "location": test_location_name,
        "date_from": date_from,
        "date_to": date_to,
    }
    response = client.post("/events/", json=payload)
    assert response.status_code == 200
    assert response.json["events"][0]["location_id"] == testing_event.location.id
    assert response.json["user_id"] == TEST_USER_ID


def test_get_event_by_id(client):
    populate(23)

    event = db.session.scalar(m.Event.select())

    response = client.get(f"/events/by_id?event_unique_id={event.unique_id}")

    assert response.status_code == 200
    assert response.json["name"] == event.name
    assert response.json["unique_id"] == event.unique_id
    assert response.json["url"] == event.url
    assert response.json["observations"] == event.observations
    assert response.json["date_time"] == event.date_time.isoformat()
