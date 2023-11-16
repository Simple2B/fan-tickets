# from .db import populate


def test_get_all_events(client_with_data):
    # populate()
    response = client_with_data.get("/events?category=festival")
    assert response
    assert response.status_code == 200
