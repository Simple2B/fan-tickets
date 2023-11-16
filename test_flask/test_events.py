from app import models as m, db


def test_get_all_events(client_with_data):
    response = client_with_data.get("/events/")
    assert response
    assert response.status_code == 200

    category = db.session.scalar(m.Category.select())
    response = client_with_data.get(f"/events/?category={category.name}")
    assert response
    assert response.status_code == 200
