from datetime import datetime, timedelta
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from .db import generate_test_users, generate_test_events
from app import db
from app import models as m


TESTING_USERS_NUMBER = 30


def test_generate_users(client: FlaskClient):
    generate_test_users(TESTING_USERS_NUMBER)
    users_list = list(db.session.scalars(m.User.select()).all())
    assert len(users_list) == TESTING_USERS_NUMBER + 1


def test_generate_events(client: FlaskClient):
    generate_test_events()
    locations_query = m.Location.select()
    locations = list(db.session.scalars(locations_query))
    assert len(locations) == 6
    events_query = m.Event.select()
    events = list(db.session.scalars(events_query))
    assert len(events) == 12
    tickets_query = m.Ticket.select()
    tickets = list(db.session.scalars(tickets_query))
    assert len(tickets) == 144


def test_delete_user(runner: FlaskCliRunner):
    db_populate_output: Result = runner.invoke(args=["db-populate"])
    assert "populated by" in db_populate_output.stdout

    all_users_before = db.session.scalars(m.User.select()).all()

    payment: m.Payment = db.session.scalar(m.Payment.select())
    assert payment
    user: m.User = payment.buyer
    assert user

    delete_command_output: Result = runner.invoke(args=["delete-user", f"--email={user.email}"])
    assert delete_command_output

    all_users_after = db.session.scalars(m.User.select().where(m.User.is_deleted.is_(False))).all()

    assert len(all_users_before) == len(all_users_after) + 1


def test_delete_obsolete_rooms(runner: FlaskCliRunner):
    TESTING_ROOMS_NUMBER = 5
    for _ in range(TESTING_ROOMS_NUMBER):
        room: m.Room = m.Room().save()
        room.created_at = datetime.now() - timedelta(days=3)

    delete_command_output: Result = runner.invoke(args=["delete-rooms"])
    assert f"{TESTING_ROOMS_NUMBER} rooms to delete" in delete_command_output.stdout
    assert "0 rooms left" in delete_command_output.stdout
