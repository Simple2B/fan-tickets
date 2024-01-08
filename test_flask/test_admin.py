import os
from io import BytesIO
from PIL import Image
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
from app import models as m
from test_flask.utils import login


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
