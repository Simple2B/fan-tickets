from .db import populate
from app import db
from app import models as m


TESTING_USERS_NUMBER = 100


def test_db_populate(client):
    populate(TESTING_USERS_NUMBER)
    users_list = list(db.session.scalars(m.User.select()).all())
    assert len(users_list) == TESTING_USERS_NUMBER + 1
    admins_query = m.User.select().where(m.User.role == m.UserRole.admin.value)
    admins = list(db.session.scalars(admins_query))
    assert len(admins) == 1
    locations_query = m.Location.select()
    locations = list(db.session.scalars(locations_query))
    assert len(locations) == 6
    events_query = m.Event.select()
    events = list(db.session.scalars(events_query))
    assert len(events) == 12
