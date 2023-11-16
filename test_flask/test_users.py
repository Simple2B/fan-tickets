from flask import current_app as app
from flask_login import current_user
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import models as m, db
from test_flask.utils import login


def test_list(client_with_data: FlaskClient):
    login(client_with_data)
    DEFAULT_PAGE_SIZE = app.config["DEFAULT_PAGE_SIZE"]
    response = client_with_data.get("/user/")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    users = db.session.scalars(m.User.select().order_by(m.User.id).limit(11)).all()
    assert len(users) == 11
    for user in users[:DEFAULT_PAGE_SIZE]:
        assert user.username in html
    assert users[10].username not in html

    client_with_data.application.config["PAGE_LINKS_NUMBER"] = 6
    response = client_with_data.get("/user/?page=6")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    assert "/user/?page=6" in html
    assert "/user/?page=3" in html
    assert "/user/?page=10" not in html


def test_create_admin(runner: FlaskCliRunner):
    res: Result = runner.invoke(args=["create-admin"])
    assert "admin created" in res.output
    query = m.User.select().where(m.User.username == app.config["ADMIN_USERNAME"])
    assert db.session.scalar(query)


def test_delete_user(client: FlaskClient):
    login(client)
    uc = db.session.query(m.User).count()
    response = client.delete("/user/delete/1")
    assert db.session.query(m.User).count() < uc
    assert response.status_code == 200


def test_user_profile(client: FlaskClient):
    login(client)
    response = client.get(f"/user/{current_user.unique_id}")
    assert response.status_code == 200
    # assert "Profile" in response.data.decode()

    response = client.get("/user/left_unique_id")
    assert response.status_code == 302
    assert response.location == f"/user/{current_user.unique_id}"
