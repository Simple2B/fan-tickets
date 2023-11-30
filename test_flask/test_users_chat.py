from flask import current_app as app
from flask_login import current_user
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import models as m, db
from test_flask.utils import login


def test_users_chat(client: FlaskClient):
    """
    Questions from the chat to the user:
    - Are you looking for buying or selling tickets or searching for events information?

    If selling then at once the user is asked to register.
    If buying then the user is asked to register after he wants to make a subscription or payment.
    Just searching for an event or a ticket does not require registration.

    Also after user chooses selling he gets in his chat window previous dialog as messages.
    And then the new dialog about registration starts.

    Registration questions:
    - What is the user's name?
    - What is your email?
    - Password
    - Confirm password
    - What is your phone number?
    - What is your bank card number?
    - Please upload your photo

    Search for events:
    - What kind of event are you looking for? (music, sports, theater, etc.)
    - What is the location of the event?
    - What is the name of the event?
    - What is the date range of the event? (date_from, date_to)
    """
    login(client)
    response = client.get("/chat/sell")
    assert response.status_code == 200
    # assert "profile" in response.data.decode()
    # assert "Endereço de Email" in response.data.decode()
