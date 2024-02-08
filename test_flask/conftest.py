import os
import re
import json
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, pagarme_client
from app.database import db
from app.commands import init_shell_commands
from test_flask.utils import register
from .db import populate

PRAGMA_GET_DATA_MOCK_MAP = {
    "customers": "customers.json",
}


@pytest.fixture(scope="session")
def flask_app(session_mocker):
    app = create_app("testing")
    app.config.update(
        {
            "TESTING": True,
        }
    )
    os.environ["APP_ENV"] = "testing"
    # os.environ["_BARD_API_KEY"] = "some_bard_key."
    print('os.environ.get("PAGARME_CONNECTION")', os.environ.get("PAGARME_CONNECTION"))

    # Mock sse
    session_mocker.patch("flask_sse.sse.publish", return_value="mocked value")

    return app


@pytest.fixture()
def app(flask_app, requests_mock):
    # mock requests
    ## pagarme
    for endpoint, json_file in PRAGMA_GET_DATA_MOCK_MAP.items():
        with open(Path("test_flask") / "assets" / "pagarme" / json_file, "r") as json_f:
            data_mocked = json.load(json_f)
        requests_mock.get(re.compile(pagarme_client.__generate_url__(endpoint)), json=data_mocked)

    yield flask_app


@pytest.fixture()
def client(app: Flask):
    with app.test_client() as client, app.app_context():
        db.drop_all()
        db.create_all()
        register()

        yield client
        db.drop_all()


@pytest.fixture()
def runner(app):
    init_shell_commands(app)
    yield app.test_cli_runner()


@pytest.fixture
def client_with_data(client: FlaskClient):
    populate()
    yield client
    db.session.rollback()
