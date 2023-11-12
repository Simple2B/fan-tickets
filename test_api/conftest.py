from random import randint
from typing import Generator
import pytest
from dotenv import load_dotenv

load_dotenv("test_api/test.env")

# flake8: noqa F402
from fastapi.testclient import TestClient
from sqlalchemy import orm

from app import models as m
from app import schema as s

from api import app
from .test_data import TestData


NUM_TEST_USERS = 30


def generate_test_users(num_objects: int = NUM_TEST_USERS, session: orm.Session = None):
    from faker import Faker

    fake = Faker()

    DOMAINS = ("com", "com.br", "net", "net.br", "org", "org.br", "gov", "gov.br")

    for i in range(num_objects):
        first_name = fake.first_name()
        last_name = fake.last_name()
        company = fake.company().split()[0].strip(",")
        dns_org = fake.random_choices(elements=DOMAINS, length=1)[0]
        email = f"{first_name.lower()}.{last_name.lower()}@{company.lower()}.{dns_org}"
        role = m.UserRole.admin if i < 3 else m.UserRole.client
        activated = True if i - num_objects == 3 else False
        user = m.User(
            username=f"{first_name}{last_name}{randint(10, 99)}",
            email=email,
            role=role.value,
            password="pass",
            activated=activated,
        )
        session.add(user)
    session.commit()


@pytest.fixture
def db(test_data: TestData) -> Generator[orm.Session, None, None]:
    from app.database import db, get_db

    with db.Session() as session:
        db.Model.metadata.drop_all(bind=session.bind)
        db.Model.metadata.create_all(bind=session.bind)
        for test_user in test_data.test_users:
            user = m.User(
                username=test_user.username,
                email=test_user.email,
                password=test_user.password,
            )
            session.add(user)
        session.commit()
        # generate_test_users(session=session)

        def override_get_db() -> Generator:
            yield session

        app.dependency_overrides[get_db] = override_get_db
        yield session
        # clean up
        db.Model.metadata.drop_all(bind=session.bind)


@pytest.fixture
def client(db) -> Generator[TestClient, None, None]:
    """Returns a non-authorized test client for the API"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_data() -> Generator[TestData, None, None]:
    """Returns a TestData object"""
    with open("test_api/test_data.json", "r") as f:
        yield TestData.model_validate_json(f.read())


@pytest.fixture
def headers(
    client: TestClient,
    test_data: TestData,
) -> Generator[dict[str, str], None, None]:
    """Returns an authorized test client for the API"""
    user = test_data.test_users[0]
    response = client.post(
        "/api/auth/login",
        data={
            "username": user.username,
            "password": user.password,
        },
    )
    assert response.status_code == 200
    token = s.Token.model_validate(response.json())

    yield dict(Authorization=f"Bearer {token.access_token}")
