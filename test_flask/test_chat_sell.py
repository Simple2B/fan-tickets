import pytest
from flask import current_app as app
from flask.testing import FlaskClient
from flask_login import current_user
from app import models as m, schema as s, db
from test_flask.utils import login
from app.controllers import get_event_by_name_bard


# @pytest.mark.skipif(True, reason="no Bard API key provided")
def test_bard_get_event_by_name(client_with_data: FlaskClient):
    seller = db.session.scalar(m.User.select())
    room = m.Room(
        seller_id=seller.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    # params = s.ChatSellEventParams(event_name="afterlife sao paulo 2024", room_unique_id=room.unique_id)
    params = s.ChatSellEventParams(event_name="Turnstile latin america 2024", room_unique_id=room.unique_id)
    response = get_event_by_name_bard(params, room)
    assert response


@pytest.mark.skipif(True, reason="no Bard API key provided")
def test_get_event_with_bard(client_with_data: FlaskClient):
    login(client_with_data)

    TESTING_EVENTS = [
        "afterlife sao paulo 2024",
        "Coldplay Brasil 2024",
        "Queen Brasil 2024",
        "Justin Bieber Brasil 2024",
        "Dua Lipa Brasil 2024",
        "Lollapalooza Brasil 2024",
        "Gorillaz Brasil 2024",
        "Twice Brasil 2024",
    ]

    # TEST_EVENT_NAME = random.choice(TESTING_EVENTS)
    TEST_EVENT_NAME = TESTING_EVENTS[5]

    room = m.Room(
        seller_id=current_user.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    response = client_with_data.get(
        f"/sell/get_event_name?room_unique_id={room.unique_id}&event_category_id=Show&user_message={TEST_EVENT_NAME}"
    )
    assert response.status_code == 200
    assert "Please provide us with a link of even" in response.text


def test_get_events_from_db(client_with_data: FlaskClient):
    login(client_with_data)

    TEST_EVENT_NAME = "Paulo Shows 2"

    room = m.Room(
        seller_id=current_user.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    response = client_with_data.get(
        f"/sell/get_event_name?room_unique_id={room.unique_id}&event_category_id=Show&user_message={TEST_EVENT_NAME}"
    )
    assert response.status_code == 200
    assert response


# def test_chat_sell_create_event(client_with_data: FlaskClient):
#     login(client_with_data)
#     response = client_with_data.get("/sell/create_event")
#     assert response.status_code == 200
#     assert "Form submitting error" in response.data.decode()

#     room = m.Room(
#         seller_id=current_user.id,
#         buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
#     ).save()
#     event = db.session.scalar(m.Event.select())
#     event_date = event.date_time.strftime(app.config["DATE_PICKER_FORMAT"])
#     response = client_with_data.get(
#         f"/sell/create_event?room_unique_id={room.unique_id}&event_location={event.location.name}&event_date={event_date}&event_name={event.name}&event_category={event.category.name}&event_url={event.url}"
#     )
#     assert response.status_code == 200
#     assert "Please, input ticket details." in response.data.decode()


# def test_chat_sell_ticket_form(client_with_data: FlaskClient):
#     login(client_with_data)
#     room = m.Room(
#         seller_id=current_user.id,
#         buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
#     ).save()
#     event = db.session.scalar(m.Event.select())
#     response = client_with_data.get(f"/sell/ticket_form?room_unique_id={room.unique_id}&event_id={event.unique_id}")
#     assert response.status_code == 200
#     assert "Please, input ticket details." in response.data.decode()


# def test_chat_sell_create_ticket(client_with_data: FlaskClient):
#     login(client_with_data)
#     room = m.Room(
#         seller_id=current_user.id,
#         buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
#     ).save()
#     event = db.session.scalar(m.Event.select())
#     TSEC = "section"
#     TQ = "queue"
#     TSEAT = "seat"
#     TQTY = 2
#     TPRICE = 100.0

#     response = client_with_data.get(
#         f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&queue={TQ}&seat={TSEAT}&quantity={TQTY}&price={TPRICE}"
#     )
#     assert response.status_code == 200
#     assert "No section provided" in response.data.decode()

#     response = client_with_data.get(
#         f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&seat={TSEAT}&quantity={TQTY}&price={TPRICE}"
#     )
#     assert response.status_code == 200
#     assert "No queue provided" in response.data.decode()

#     response = client_with_data.get(
#         f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&queue={TQ}&quantity={TQTY}&price={TPRICE}"
#     )
#     assert response.status_code == 200
#     assert "No seat provided" in response.data.decode()

#     response = client_with_data.get(
#         f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&queue={TQ}&seat={TSEAT}&price={TPRICE}"
#     )
#     assert response.status_code == 200
#     assert "No quantity provided" in response.data.decode()

#     response = client_with_data.get(
#         f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&queue={TQ}&seat={TSEAT}&quantity={TQTY}"
#     )
#     assert response.status_code == 200
#     assert "No price provided" in response.data.decode()

#     response = client_with_data.get(
#         f"/sell/create_ticket?room_unique_id={room.unique_id}&event_id={event.unique_id}&section={TSEC}&queue={TQ}&seat={TSEAT}&quantity={TQTY}&price={TPRICE}"
#     )
#     assert response.status_code == 200
#     assert "You have successfully created a ticket" in response.data.decode()
