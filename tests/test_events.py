from datetime import timedelta
from .db import populate
from app import db
from app import models as m


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

    payload.pop("user_id")
    response = client.post("/events/", json=payload)
    assert response.status_code == 400
    assert "Missing user_id" in response.json["details"]
    assert "BAD_REQUEST" in response.json["error"]

    payload = {
        "user_id": TEST_USER_ID,
        "token": "testing_whatsapp_token",
        "location": test_location_name,
        "date_from": date_from,
        "date_to": date_to,
    }


def test_get_event_by_id(client):
    populate(23)

    event = db.session.scalar(m.Event.select())

    response = client.get(f"/events/by_id?event_unique_id={event.unique_id}")
    assert response.status_code == 200
    assert response.json["name"] == event.name
    assert response.json["unique_id"] == event.unique_id
    assert response.json["url"] == event.url
    assert response.json["observations"] == event.observations
