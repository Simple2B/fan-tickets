def test_main_page(client):
    response = client.get("/")
    assert response
    assert response.status_code == 200


def test_help_page(client):
    response = client.get("/help")
    assert response
    assert response.status_code == 200
