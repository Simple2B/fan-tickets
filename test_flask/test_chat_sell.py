from flask import current_app as app
from flask.testing import FlaskClient
from flask_login import current_user
from app import models as m, db
from test_flask.utils import login


def test_chat_sell_get_events(client_with_data: FlaskClient):
    login(client_with_data)
    response = client_with_data.get("/sell/")
    assert response.status_code == 200
    assert "No event location provided" in response.data.decode()

    event = db.session.scalar(m.Event.select())
    response = client_with_data.get(f"/sell/?event_location={event.location.name}")
    assert response.status_code == 200
    assert "No event date provided" in response.data.decode()

    event_date = event.date_time.strftime(app.config["DATE_PICKER_FORMAT"])
    response = client_with_data.get(f"/sell/?event_location=left_location&event_date={event_date}")
    assert response.status_code == 200
    assert "There is no such events in our database" in response.data.decode()

    response = client_with_data.get(f"/sell/?event_location={event.location.name}&event_date={event_date}")
    assert response.status_code == 200
    assert "Choose an event from the list." in response.data.decode()


def test_chat_sell_event_form(client_with_data: FlaskClient):
    login(client_with_data)
    response = client_with_data.get("/sell/event_form")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    room = m.Room(
        seller_id=current_user.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    response = client_with_data.post(f"/sell/event_form?room_unique_id={room.unique_id}")
    assert "No event location provided" in response.data.decode()

    # response = client_with_data.post(f"/sell/event_form?room_unique_id={room.unique_id}&event_location=left_location")
