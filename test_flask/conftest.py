import os
import re
import json
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, pagarme_client
from app.database import db
from test_flask.utils import register
from .db import populate


PRAGMA_GET_DATA_MOCK_MAP = {
    "customers": "customers.json",
}


@pytest.fixture()
# def app(requests_mock):
def app():
    app = create_app("testing")
    # pagarme_client.self.__generate_url__("customers", customer_list_query)
    app.config.update(
        {
            "TESTING": True,
        }
    )
    os.environ["APP_ENV"] = "testing"
    # os.environ["_BARD_API_KEY"] = "some_bard_key."
    print('os.environ.get("PAGARME_CONNECTION")', os.environ.get("PAGARME_CONNECTION"))

    # mock requests
    ## pagarme
    # for endpoint, json_file in PRAGMA_GET_DATA_MOCK_MAP.items():
    #     with open(Path("test_flask") / "assets" / "pagarme" / json_file, "r") as json_f:
    #         data_mocked = json.load(json_f)
    #     requests_mock.get(re.compile(pagarme_client.__generate_url__(endpoint)), json=data_mocked)

    yield app


@pytest.fixture()
def client(app: Flask):
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()

        db.drop_all()
        db.create_all()
        register()

        yield client
        db.drop_all()
        app_ctx.pop()


@pytest.fixture()
def runner(app, client):
    from app import commands

    commands.init(app)

    yield app.test_cli_runner()


@pytest.fixture
def client_with_data(client: FlaskClient):
    populate()
    yield client
    db.session.rollback()
