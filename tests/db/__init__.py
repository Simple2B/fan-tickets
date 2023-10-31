from typing import Generator
from faker import Faker
from sqlalchemy import func
from app import db
from app import models as m


faker = Faker()

NUM_TEST_USERS = 100
NUM_TEST_LOCATIONS = 6
NUM_TEST_CATEGORY = 5
NUM_TEST_EVENTS = 12


def gen_test_items(num_objects: int) -> Generator[str, None, None]:
    from faker import Faker

    fake = Faker()

    DOMAINS = ("com", "com.br", "net", "net.br", "org", "org.br", "gov", "gov.br")

    i = db.session.query(func.max(m.User.id)).scalar()

    for _ in range(num_objects):
        i += 1
        # Primary name
        first_name = fake.first_name()

        # Secondary name
        last_name = fake.last_name()

        company = fake.company().split()[0].strip(",")

        # Company DNS
        dns_org = fake.random_choices(elements=DOMAINS, length=1)[0]

        # email formatting
        yield i, f"{first_name}{i}".lower(), f"{first_name}.{last_name}{i}@{company}.{dns_org}".lower()


def populate(count: int = NUM_TEST_USERS):
    for index, username, email in gen_test_items(count):
        role = m.UserRole.admin if index < 3 else m.UserRole.client
        m.User(
            username=username,
            email=email,
            role=role.value,
        ).save(False)

    for _ in range(NUM_TEST_LOCATIONS):
        m.Location(
            name=faker.city(),
        ).save(False)

    for i in range(NUM_TEST_CATEGORY):
        m.Category(name=f"Category {i + 1}").save(False)

    for i in range(NUM_TEST_EVENTS):
        m.Event(
            name=faker.sentence(nb_words=3),
            url=faker.url(),
            observations=f"Description for event {i + 1}",
            location_id=faker.random_int(min=1, max=NUM_TEST_LOCATIONS),
            category_id=faker.random_int(min=1, max=NUM_TEST_CATEGORY),
            date_time=faker.date_time_between(start_date="-1m", end_date="+1m"),
        ).save(False)

    db.session.commit()
