import os
import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db
from test_flask.utils import register
from .db import populate


@pytest.fixture()
def app():
    app = create_app("testing")
    app.config.update(
        {
            "TESTING": True,
        }
    )
    os.environ["APP_ENV"] = "testing"
    os.environ["_BARD_API_KEY"] = "some_bard_key."

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
