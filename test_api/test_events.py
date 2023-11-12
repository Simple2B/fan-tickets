import pytest

from fastapi.testclient import TestClient

# from app import schema as s
from config import config

from .test_data import TestData

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_event_by_id(
    client: TestClient,
    headers: dict[str, str],
    test_data: TestData,
):
    response = client.get(
        "/api/events/by_id?event_unique_id=some-unique-id",
        headers=headers,
    )
    assert response.status_code == 200
