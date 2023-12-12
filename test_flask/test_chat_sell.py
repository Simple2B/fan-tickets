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

    event = db.session.scalar(m.Event.select())
    event_date = event.date_time.strftime(app.config["DATE_PICKER_FORMAT"])
    response = client_with_data.post(
        f"/sell/event_form?room_unique_id={room.unique_id}&event_location={event.location.name}&event_date={event_date}"
    )
    assert response.status_code == 200
    assert "Please, input event details." in response.data.decode()


def test_chat_sell_create_event(client_with_data: FlaskClient):
    login(client_with_data)
    response = client_with_data.get("/sell/create_event")
    assert response.status_code == 200
    assert "Form submitting error" in response.data.decode()

    room = m.Room(
        seller_id=current_user.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    event = db.session.scalar(m.Event.select())
    event_date = event.date_time.strftime(app.config["DATE_PICKER_FORMAT"])
    response = client_with_data.get(
        f"/sell/create_event?room_unique_id={room.unique_id}&event_location={event.location.name}&event_date={event_date}&event_name={event.name}&event_category={event.category.name}&event_url={event.url}"
    )
    assert response.status_code == 200
    assert "Please, input ticket details." in response.data.decode()


def test_chat_sell_ticket_form(client_with_data: FlaskClient):
    login(client_with_data)
    room = m.Room(
        seller_id=current_user.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    event = db.session.scalar(m.Event.select())
    response = client_with_data.get(f"/sell/ticket_form?room_unique_id={room.unique_id}&event_id={event.unique_id}")
    assert response.status_code == 200
    assert "Please, input ticket details." in response.data.decode()


def test_chat_sell_create_ticket(client_with_data: FlaskClient):
    login(client_with_data)
    room = m.Room(
        seller_id=current_user.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    event = db.session.scalar(m.Event.select())
    TSEC = "section"
    TQ = "queue"
    TSEAT = "seat"
    TQTY = 2
    TPRICE = 100.0

    response = client_with_data.get(
        f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&queue={TQ}&seat={TSEAT}&quantity={TQTY}&price={TPRICE}"
    )
    assert response.status_code == 200
    assert "No section provided" in response.data.decode()

    response = client_with_data.get(
        f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&seat={TSEAT}&quantity={TQTY}&price={TPRICE}"
    )
    assert response.status_code == 200
    assert "No queue provided" in response.data.decode()

    response = client_with_data.get(
        f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&queue={TQ}&quantity={TQTY}&price={TPRICE}"
    )
    assert response.status_code == 200
    assert "No seat provided" in response.data.decode()

    response = client_with_data.get(
        f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&queue={TQ}&seat={TSEAT}&price={TPRICE}"
    )
    assert response.status_code == 200
    assert "No quantity provided" in response.data.decode()

    response = client_with_data.get(
        f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&queue={TQ}&seat={TSEAT}&quantity={TQTY}"
    )
    assert response.status_code == 200
    assert "No price provided" in response.data.decode()

    response = client_with_data.get(
        f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&queue={TQ}&seat={TSEAT}&quantity={TQTY}&price={TPRICE}"
    )
    assert response.status_code == 200
    assert "You have successfully created a ticket" in response.data.decode()
