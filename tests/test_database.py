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
    reviews_query = m.Review.select()
    reviews = list(db.session.scalars(reviews_query))
    assert len(reviews) == TESTING_USERS_NUMBER * 2 + 2


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


def test_whatsapp_endpoint(client, monkeypatch):
    # def send_events_to_webhook(*args, **kwargs):
    #     return

    # monkeypatch.setattr("app.views.main.send_events_to_webhook", send_events_to_webhook)

    populate(23)

    TEST_USER_ID = 380934323377
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
    response = client.post("/whatsapp", json=payload)
    assert response.status_code == 200
    assert response.json
