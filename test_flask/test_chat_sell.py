import pytest
from flask import current_app as app
from flask.testing import FlaskClient
from flask_login import current_user
from app import models as m, schema as s, db
from test_flask.utils import login
from app.controllers import get_event_by_name_bard
from app.controllers.chat_sell import (
    ask_bard_for_event,
    parse_bard_response,
    parse_date_with_bard,
    parse_time_with_bard,
    create_event_date_time,
)


@pytest.mark.skipif(True, reason="no Bard API key provided")
def test_ask_bard_for_event():
    response = ask_bard_for_event("Coldplay")
    assert response


def test_parse_bard_response():
    # bard_response = '{\n "event_name": "Rock in Rio 2024",\n "official_url": "https://rockinrio.com/",\n "location": "Rio de Janeiro",\n "venue": "Cidade do Rock",\n "date": "2024-09-27",\n "time": "18:00"\n}'
    # bard_response = '{\n  "event_name": "Lollapalooza Brasil",\n  "official_url": "https://www.lollapaloozabr.com/",\n  "location": "São Paulo",\n  "venue": "Autódromo de Interlagos",\n  "date": "2023-03-24",\n  "time": "13:00"\n}'
    # bard_response = 'Yes, there is an event in Brazil with a name similar to "Warung day festival".\n\n```\n{\n  "event_name": "Warung Beach Club Day Festival",\n  "official_url": "https://www.warungbeachclub.com.br/eventos/",\n  "location": "Praia de Jurerê Internacional, Florianópolis, Santa Catarina",\n  "venue": "Warung Beach Club",\n  "date": "2023-01-01",\n  "time": "12:00"\n}\n```'
    # bard_response = 'Yes, there is an event in Brazil with a name similar to "Turnstile Latin America 2024". It is called "Turnstile Latin America 2023". Here are the details of the event:\n\n```\n{\n  "event_name": "Turnstile Latin America 2023",\n  "official_url": "https://www.turnstilelatinamerica.com/",\n  "location": "São Paulo, Brazil",\n  "venue": "São Paulo Expo",\n  "date": "2023-05-23",\n  "time": "10:00 AM - 6:00 PM"\n}\n```'
    # bard_response = 'Yes, there is an event in Brazil that has a name similar to "Metallica". Here are the details:\n\n```\n{\n  "event_name": "Metallica: WorldWired Tour 2023",\n  "official_url": "https://www.metallica.com/tour/",\n  "location": "São Paulo, Brazil",\n  "venue": "Estádio do Morumbi",\n  "date": "2023-05-12",\n  "time": "20:00"\n}\n```'
    bard_response = '{\n  "event_name": "Brunch Electronik São Paulo",\n  "official_url": "https://brunchelectronik.com.br/sao-paulo/",\n  "location": "São Paulo, Brazil",\n  "venue": "São Paulo Expo",\n  "date": "2023-12-02",\n  "time": "12:00 - 22:00"\n}'
    # bard_response = '{\n  "event_name": "Rock in Rio",\n  "official_url": "https://rockinrio.com/",\n  "location": "Rio de Janeiro",\n  "venue": "Cidade do Rock",\n  "date": "September 2-11, 2022",\n  "time": "Starting at 7 pm"\n}'
    # bard_response = "Sorry, I couldn't find any event with a name similar to 'Coldplay' in Brazil. Please provide me with a link of the event."

    response_result, parsed_successfully = parse_bard_response(bard_response)
    assert response_result


@pytest.mark.skipif(True, reason="no Bard API key provided")
def test_parse_date_with_bard():
    DATE_TO_PARSE = "September 2-11, 2022"
    date_parse_response = parse_date_with_bard(DATE_TO_PARSE)
    assert date_parse_response


@pytest.mark.skipif(True, reason="no Bard API key provided")
def test_parse_time_with_bard():
    # TIME_TO_PARSE = "Starting at 7 pm"
    # TIME_TO_PARSE = "Gates open at 5 pm"
    TIME_TO_PARSE = "Event will last from 8 pm to 2 am"
    time_parse_response = parse_time_with_bard(TIME_TO_PARSE)
    assert time_parse_response


def test_create_event_date_time():
    event_date = "2023-03-24"
    event_time = "13:00"
    event_date_time = create_event_date_time(event_date, event_time)
    assert event_date_time


@pytest.mark.skipif(True, reason="no Bard API key provided")
def test_bard_get_event_by_name(client_with_data: FlaskClient):
    room = m.Room(
        seller_id=current_user.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()
    params = s.ChatSellEventParams(event_name="afterlife sao paulo 2024", room_unique_id=room.unique_id)
    # response = get_event_by_name_bard("afterlife sao paulo 2024")
    # response = get_event_by_name_bard("metallica rio de janeiro 2024")
    # response = get_event_by_name_bard("Turnstile latin america 2024")
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


def test_get_ticket_price(client_with_data: FlaskClient):
    login(client_with_data)
    user: m.User = current_user
    ticket: m.Ticket = db.session.scalar(m.Ticket.select())
    ticket.event.creator_id = user.id
    ticket.seller_id = user.id
    ticket.price_net = None
    ticket.price_gross = None
    db.session.commit()

    room = m.Room(
        seller_id=user.id,
        buyer_id=app.config["CHAT_DEFAULT_BOT_ID"],
    ).save()

    TEST_PRICE_NET = 100
    response = client_with_data.get(
        f"/sell/get_ticket_price?ticket_unique_id={ticket.unique_id}&room_unique_id={room.unique_id}&user_message={TEST_PRICE_NET}"
    )
    assert response.status_code == 200
    assert ticket.price_net == TEST_PRICE_NET
