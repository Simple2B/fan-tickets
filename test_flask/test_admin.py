from PIL import Image
from io import BytesIO
from flask.testing import FlaskClient
from test_flask.utils import login
from app import models as m
from werkzeug.datastructures import FileStorage


def test_picture_upload(client: FlaskClient):
    previous_images_number = m.Picture.count()

    # Create a mock image file
    img_byte_arr = BytesIO()
    img = Image.new("RGB", (60, 30), color="red")
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    data = {"file": (img_byte_arr, "test.png")}

    login(client)
    response = client.post(
        "/admin/picture-upload", content_type="multipart/form-data", data=data
    )

    assert response.status_code == 200
    assert response.json["image upload status"] == "success"
    assert m.Picture.count() == previous_images_number + 1

    previous_images_number = m.Picture.count()

    with open("test_flask/fan_ticket_logo.jpg", "rb") as img_file:
        data = {"file": FileStorage(img_file, "fan_ticket_logo.jpg")}

        login(client)
        response = client.post(
            "/admin/picture-upload", content_type="multipart/form-data", data=data
        )

        assert response.status_code == 200
        assert response.json["image upload status"] == "success"
        assert m.Picture.count() == previous_images_number + 1
