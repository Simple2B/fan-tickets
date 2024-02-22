import os
from datetime import timedelta
from random import randint, choice
from faker import Faker
from app.database import db
from app import models as m
from app.logger import log
from app.models.utils import utcnow
from app.controllers.notification_client import NotificationType

faker = Faker()

NUM_TEST_USERS = 50
TEST_LOCATIONS = [
    "Rio de Janeiro",
    "São Paulo",
    "Belo Horizonte",
    "Brasília",
    "Salvador",
    "Curitiba",
]
TEST_CATEGORIES = [
    "Shows",
    "Festivais",
    "Esportes",
    "Other",
]
NUM_TEST_EVENTS = 12
TEST_TICKET_TYPES = [
    m.TicketType.GENERAL.value,
    m.TicketType.TRACK.value,
    m.TicketType.BOX.value,
    m.TicketType.BACK_STAGE.value,
]
TEST_TICKET_CATEGORIES = [
    m.TicketCategory.STUDENT.value,
    m.TicketCategory.ELDERLY.value,
    m.TicketCategory.SOCIAL.value,
    m.TicketCategory.OTHER.value,
]


def generate_test_users(num_objects: int = NUM_TEST_USERS):
    from faker import Faker

    fake = Faker()

    DOMAINS = ("com", "com.br", "net", "net.br", "org", "org.br", "gov", "gov.br")

    for i in range(num_objects):
        first_name = fake.first_name()
        last_name = fake.last_name()
        company = fake.company().split()[0].strip(",")
        dns_org = fake.random_choices(elements=DOMAINS, length=1)[0]
        email = f"{first_name.lower()}.{last_name.lower()}@{company.lower()}.{dns_org}"
        role = m.UserRole.client
        user = m.User(
            username=f"{first_name}{last_name}{randint(10, 99)}",
            name=first_name,
            last_name=last_name,
            email=email,
            phone=fake.phone_number(),
            card=faker.random_number(digits=16, fix_len=True),
            role=role.value,
            # password="pass",
            activated=True,
            birth_date=utcnow() - timedelta(days=365 * randint(18, 60)),
        ).save(commit=False)
        log(log.INFO, "User generated: [%s]", user)

        # notification_config = m.NotificationsConfig(user_id=user.id)
        # db.session.add(notification_config)
        m.NotificationsConfig(user=user).save(False)
    db.session.commit()
    users_number = m.User.count()
    log(log.INFO, "[%d] users generated", users_number)


def generate_test_events(num_objects: int = NUM_TEST_EVENTS):
    FOLDER_PATH = "test_flask/locations_pictures"  # replace with your folder path

    location_picture_ids = []
    for filename in os.listdir(FOLDER_PATH):
        if ".png" in filename:
            with open(f"{FOLDER_PATH}/{filename}", "rb") as img_file:
                filename = filename.split(".")[0]
                picture = m.Picture(
                    filename=filename,
                    file=img_file.read(),
                    mimetype="png",
                ).save()
                location_picture_ids.append(picture.id)
    print(location_picture_ids)
    test_locations: list[m.Location] = []
    for location_name in TEST_LOCATIONS:
        location = m.Location(
            name=location_name,
            picture_id=choice(location_picture_ids),
        ).save(False)
        test_locations.append(location)
    test_categories: list[m.Category] = []
    for category_name in TEST_CATEGORIES:
        category = m.Category(
            name=category_name,
        ).save(False)
        test_categories.append(category)
    for i in range(NUM_TEST_EVENTS):
        location_id = randint(1, len(TEST_LOCATIONS))
        location_name = test_locations[location_id - 1].name
        category_id = randint(1, len(TEST_CATEGORIES))
        category_name = test_categories[category_id - 1].name
        # seller_id = randint(1, NUM_TEST_USERS)
        # buyer_id = randint(1, NUM_TEST_USERS)

        seller_id = 3
        buyer_id = 4

        # set to seller a recipient_id
        # seller: m.User = db.session.get(m.User, seller_id)
        # if seller:
        #     seller.recipient_id = "re_clsnbbg4c071b019twu0zvkio"
        #     seller.save(False)

        event = m.Event(
            name=f"{location_name} {category_name} {i}",
            url=f"https://{location_name.lower().replace(' ', '-')}-{category_name.lower().replace(' ', '-')}-{i}.com",
            observations=faker.text(max_nb_chars=200),
            warning="don't forget to bring your ID",
            location_id=location_id,
            venue=f"{location_name} venue {i}",
            category_id=category_id,
            creator_id=seller_id,
            date_time=utcnow() + timedelta(days=randint(10, 30)),
            approved=True,
        ).save(False)
        for j in range(12):
            # price_net = randint(10, 1000)
            price_net = 1
            price_gross = int(round(price_net * 1.11))
            is_in_cart = True if j <= 1 else False
            is_reserved = True if 2 <= j <= 4 else False
            is_sold = True if 5 <= j <= 7 else False
            ticket = m.Ticket(
                event=event,
                description=faker.text(max_nb_chars=200),
                ticket_type=TEST_TICKET_TYPES[randint(0, 2)],
                ticket_category=TEST_TICKET_CATEGORIES[randint(0, 2)],
                warning=faker.text(max_nb_chars=200),
                section=f"Section {j}",
                queue=f"Queue {j}",
                seat=f"Seat {j}",
                price_net=price_net,
                price_gross=price_gross,
                quantity=randint(1, 4),
                is_in_cart=is_in_cart,
                is_reserved=is_reserved,
                is_sold=is_sold,
                seller_id=seller_id,
                buyer_id=buyer_id,
            ).save(False)
            m.Notification(
                notification_type=NotificationType.TICKET_PUBLISHED.value,
                payload={"data": f"Dispute created for ticket {ticket.unique_id} of user {seller_id}"},
            ).save(False)
            if is_sold:
                m.Payment(
                    buyer_id=buyer_id,
                    ticket=ticket,
                    description=faker.text(max_nb_chars=200),
                ).save(False)
                m.Notification(
                    notification_type=NotificationType.TICKET_SOLD.value,
                    payload={"data": f"Ticket {ticket.unique_id} of user {seller_id} is sold"},
                ).save(False)
            if ticket.is_available:
                m.Notification(
                    notification_type=NotificationType.TICKET_AVAILABLE.value,
                    payload={"data": f"Ticket {ticket.unique_id} is available"},
                ).save(False)
    db.session.commit()


def set_users_images():
    with open("test_flask/users_pictures/users_picture_01.png", "rb") as img_file:
        picture = m.Picture(
            filename="default_avatar",
            file=img_file.read(),
            mimetype="image/png",
        ).save(False)

        users = m.User.all()
        for user in users:
            user.picture = picture
            user.save(False)
        db.session.commit()
    print("users images script worked successfully")


def set_users_identity_documents():
    with open("test_flask/users_pictures/default_passport.png", "rb") as img_file:
        picture = m.Picture(
            filename="default_passport",
            file=img_file.read(),
            mimetype="image/png",
        ).save(False)

        users = m.User.all()
        for u in users:
            user: m.User = u
            user.identity_document = picture
            user.save(False)
        db.session.commit()


def populate(count: int = NUM_TEST_USERS):
    generate_test_users()
    generate_test_events()
    set_users_images()
    set_users_identity_documents()
