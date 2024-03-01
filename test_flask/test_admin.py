import os
from io import BytesIO
from PIL import Image
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
from app import models as m, db
from config import config
from test_flask.utils import login


CFG = config()
TEST_SERVICE_FEE = 7
TEST_BANK_FEE = 8
TEST_SORTING_TYPE = "category"
SELLING_LIMIT = 7
BUYING_LIMIT = 7


def test_picture_upload(client: FlaskClient):
    previous_images_number = m.Picture.count()

    # Create a mock image file
    img_byte_arr = BytesIO()
    img = Image.new("RGB", (60, 30), color="red")
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    login(client)
    response = client.post(
        "/admin/picture-upload",
        content_type="multipart/form-data",
        data={"file": (img_byte_arr, "test.png")},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert m.Picture.count() == previous_images_number + 1

    previous_images_number = m.Picture.count()

    with open("test_flask/fan_ticket_logo.jpg", "rb") as img_file:
        data = {"file": FileStorage(img_file, "fan_ticket_logo.jpg")}

        login(client)
        response = client.post(
            "/admin/picture-upload",
            content_type="multipart/form-data",
            data=data,
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert response.json == {}
        assert m.Picture.count() == previous_images_number + 1

    previous_images_number = m.Picture.count()

    with open("test_flask/fan_ticket_logo.jpg", "rb") as img_file:
        m.Picture(
            filename="fan_ticket_logo.jpg",
            file=img_file.read(),
            mimetype="image/jpeg",
        ).save()
        assert m.Picture.count() == previous_images_number + 1


def test_location_images(client: FlaskClient):
    previous_images_number = m.Picture.count()
    folder_path = "test_flask/locations_pictures"  # replace with your folder path

    pictures = 0
    for filename in os.listdir(folder_path):
        with open(f"{folder_path}/{filename}", "rb") as img_file:
            filename = filename.split(".")[0]
            m.Picture(
                filename=filename,
                file=img_file.read(),
                mimetype="png",
            ).save()
            pictures += 1
    assert m.Picture.count() == previous_images_number + pictures


def test_events(client_with_data: FlaskClient):
    login(client_with_data)

    events_query = m.Event.select().limit(CFG.DEFAULT_PAGE_SIZE).order_by(m.Event.date_time.desc())
    events = db.session.scalars(events_query).all()
    assert len(events) == CFG.DEFAULT_PAGE_SIZE

    response = client_with_data.get("/admin/event/events")
    assert response.status_code == 200
    assert b"Events" in response.data
    assert b"Search for events" in response.data
    assert b"Location" in response.data
    assert b"Dates" in response.data
    assert b"Category" in response.data
    assert b"Status" in response.data
    assert events[0].name in response.data.decode()
    assert events[0].url in response.data.decode()
    assert events[-1].name in response.data.decode()
    assert events[-1].url in response.data.decode()


def test_individual_fee_settings(client_with_data: FlaskClient):
    login(client_with_data)
    user: m.User = db.session.scalar(m.User.select())

    get_response = client_with_data.get(f"/admin/settings/individual/{user.uuid}")
    assert get_response.status_code == 200
    assert f"{user.name} {user.last_name} - Individual fee settings" in get_response.data.decode()
    assert b"service_fee" in get_response.data
    assert b"bank_fee" in get_response.data

    post_response = client_with_data.post(
        f"/admin/settings/individual/{user.uuid}",
        data={"service_fee": TEST_SERVICE_FEE, "bank_fee": TEST_BANK_FEE},
        follow_redirects=True,
    )
    assert post_response.status_code == 200
    assert f"{user.name} {user.last_name} - Individual fee settings" in post_response.data.decode()
    assert user.service_fee == TEST_SERVICE_FEE
    assert user.bank_fee == TEST_BANK_FEE


def test_global_fee_settings(client_with_data: FlaskClient):
    login(client_with_data)

    get_response = client_with_data.get("/admin/settings/general")
    assert get_response.status_code == 200
    assert b"Global settings" in get_response.data

    post_response = client_with_data.post(
        "/admin/settings/general",
        data={
            "service_fee": TEST_SERVICE_FEE,
            "bank_fee": TEST_BANK_FEE,
            "tickets_sorting_by": TEST_SORTING_TYPE,
            "selling_limit": SELLING_LIMIT,
            "buying_limit": BUYING_LIMIT,
        },
        follow_redirects=True,
    )
    assert post_response.status_code == 200
    assert b"Global settings" in post_response.data

    global_fee_settings = db.session.scalar(m.GlobalFeeSettings.select())
    assert global_fee_settings.service_fee == TEST_SERVICE_FEE
    assert global_fee_settings.bank_fee == TEST_BANK_FEE
    assert global_fee_settings.tickets_sorting_by == TEST_SORTING_TYPE
