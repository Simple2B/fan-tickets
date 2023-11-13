from datetime import timedelta
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app import models as m
from app import schema as s
from config import config

# from .test_data import TestData


CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_all_evens(
    client: TestClient,
    headers: dict[str, str],
    db: Session,
):
    events_number = db.query(m.Event).count()
    response = client.post(
        "/api/events/",
        headers=headers,
        json={},
    )
    assert response.status_code == 200
    events = s.Events.model_validate(response.json())
    assert events_number == len(events.events)


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_events_by_location(
    client: TestClient,
    headers: dict[str, str],
    db: Session,
):
    event = db.scalar(m.Event.select())
    events_by_location = db.scalars(
        m.Event.select().where(m.Event.location == event.location)
    )
    events_by_location_number = len(list(events_by_location))
    payload = s.EventsInput(location=f"{event.location.name}").model_dump()
    response = client.post(
        "/api/events/",
        headers=headers,
        json=payload,
    )
    assert response.status_code == 200
    events = s.Events.model_validate(response.json())
    assert len(list(events.events)) == events_by_location_number


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_events_by_date_from(
    client: TestClient,
    headers: dict[str, str],
    db: Session,
):
    event = db.scalar(m.Event.select())
    events_by_date_from = db.scalars(
        m.Event.select().where(m.Event.date_time >= event.date_time)
    )
    events_by_date_from_number = len(list(events_by_date_from))
    payload = s.EventsInput(
        date_from=event.date_time.isoformat(),
    ).model_dump()
    response = client.post(
        "/api/events/",
        headers=headers,
        json=payload,
    )
    assert response.status_code == 200
    events = s.Events.model_validate(response.json())
    assert len(list(events.events)) == events_by_date_from_number


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_events_by_date_to(
    client: TestClient,
    headers: dict[str, str],
    db: Session,
):
    event = db.scalar(m.Event.select())
    # date_to = event.date_time
    # events_by_date_to = db.scalars(m.Event.select().where(m.Event.date_time <= date_to))
    # events_by_date_to_number = len(list(events_by_date_to))
    payload = s.EventsInput(
        # location=f"{event.location.name}",
        date_from=event.date_time.isoformat(),
    ).model_dump()
    response = client.post(
        "/api/events/",
        headers=headers,
        json=payload,
    )
    assert response.status_code == 200
    # events = s.Events.model_validate(response.json())
    # assert len(list(events.events)) == events_by_date_to_number


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_events_by_dates(
    client: TestClient,
    headers: dict[str, str],
    db: Session,
):
    event = db.scalar(m.Event.select())
    date_from = event.date_time - timedelta(days=1)
    date_to = event.date_time + timedelta(days=1)
    events_query = m.Event.select().where(
        m.Event.date_time >= date_from,
        m.Event.date_time <= date_to,
    )
    events_by_dates = db.scalars(events_query)
    events_by_dates_number = len(list(events_by_dates))
    payload = s.EventsInput(
        date_from=date_from.isoformat(),
        date_to=date_to.isoformat(),
    ).model_dump()
    response = client.post(
        "/api/events/",
        headers=headers,
        json=payload,
    )
    assert response.status_code == 200
    events = s.Events.model_validate(response.json())
    assert len(list(events.events)) == events_by_dates_number


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_event_by_id(
    client: TestClient,
    headers: dict[str, str],
    db: Session,
):
    event_db = db.scalar(m.Event.select())
    response = client.get(
        f"/api/events/by_id?event_unique_id={event_db.unique_id}",
        headers=headers,
    )
    assert response.status_code == 200
    event = s.Event.model_validate(response.json())
    assert event.unique_id == event_db.unique_id


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_event_wrong_id(
    client: TestClient,
    headers: dict[str, str],
    db: Session,
):
    response = client.get(
        "/api/events/by_id?event_unique_id=some-wrong-id",
        headers=headers,
    )
    assert response.status_code == 400
