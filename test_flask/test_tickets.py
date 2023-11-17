from app import models as m, db


def test_get_all_tickets(client_with_data):
    response = client_with_data.get("/tickets/")
    assert response
    assert response.status_code == 200

    location = db.session.scalar(m.Location.select())
    response = client_with_data.get(f"/tickets/?location={location.name}")
    assert response
    assert response.status_code == 200
