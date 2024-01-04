import os
from datetime import datetime, timedelta
from random import randint, choice
from faker import Faker
from app.database import db
from app import models as m
from app.logger import log


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
    "Teatro",
    "Cinema",
    "Esportes",
]
NUM_TEST_EVENTS = 12
TEST_TICKET_TYPES = [
    m.TicketType.TRACK.value,
    m.TicketType.BOX.value,
    m.TicketType.BACK_STAGE.value,
]
TEST_TICKET_CATEGORIES = [
    m.TicketCategory.LOT.value,
    m.TicketCategory.SOCIAL_ENTRY.value,
    m.TicketCategory.ENTIRE.value,
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
        role = m.UserRole.admin if i < 3 else m.UserRole.client
        # activated = True if i - num_objects == 3 else False
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
        ).save(commit=False)
        # db.session.add(user)
        # db.session.flush()
        log(log.INFO, "User generated: [%s]", user)

        # notification_config = m.NotificationsConfig(user_id=user.id)
        # db.session.add(notification_config)
        m.NotificationsConfig(user=user).save(False)
    db.session.commit()
    users_number = m.User.count()
    log(log.INFO, "[%d] users generated", users_number)

    # for i in range(users_number):
    #     review_given = m.Review(
    #         rate=randint(1, 5),
    #         text=faker.text(max_nb_chars=200),
    #         reviewer_id=i + 1,
    #         receiver_id=randint(1, users_number),
    #     )
    #     db.session.add(review_given)
    #     log(log.INFO, "Review generated: [%s]", review_given)

    #     review_got = m.Review(
    #         rate=randint(1, 5),
    #         text=faker.text(max_nb_chars=200),
    #         reviewer_id=randint(1, users_number),
    #         receiver_id=i + 1,
    #     )
    #     db.session.add(review_got)
    #     log(log.INFO, "Review generated: [%s]", review_given)
    # db.session.commit()


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
        seller_id = randint(1, NUM_TEST_USERS)
        event = m.Event(
            name=f"{location_name} {category_name} {i}",
            url=f"https://{location_name.lower().replace(' ', '-')}-{category_name.lower().replace(' ', '-')}-{i}.com",
            observations=faker.text(max_nb_chars=200),
            warning="don't forget to bring your ID",
            location_id=location_id,
            category_id=category_id,
            creator_id=seller_id,
            date_time=datetime.now() + timedelta(days=randint(-10, 100)),
        ).save(False)
        for j in range(12):
            price_net = randint(10, 1000)
            price_gross = price_net * 1.08
            is_in_cart = True if j <= 1 else False
            is_reserved = True if 2 <= j <= 4 else False
            is_sold = True if 5 <= j <= 7 else False
            buyer_id = randint(1, NUM_TEST_USERS)
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
                type_of=m.NotificationType.TICKET_PUBLISHED.value,
                text=f"Dispute created for ticket {ticket.unique_id} of user {seller_id}",
                user_id=seller_id,
            ).save(False)
            if is_sold:
                m.Payment(
                    buyer_id=buyer_id,
                    ticket=ticket,
                    description=faker.text(max_nb_chars=200),
                ).save(False)
                m.Notification(
                    type_of=m.NotificationType.TICKET_SOLD.value,
                    text=f"Ticket {ticket.unique_id} of user {seller_id} is sold",
                    user_id=seller_id,
                ).save(False)
            if ticket.is_available:
                m.Notification(
                    type_of=m.NotificationType.TICKET_AVAILABLE.value,
                    text=f"Ticket {ticket.unique_id} is available",
                    user_id=seller_id,
                ).save(False)
            # for k in range(4):
            #     type_of = m.RoomType.DISPUTE.value if k == 0 else m.RoomType.CHAT.value
            #     if type_of == m.RoomType.DISPUTE.value:
            #         m.Dispute(
            #             description=faker.text(max_nb_chars=200),
            #             is_active=True,
            #             buyer_id=buyer_id,
            #             ticket_id=ticket.id,
            #         ).save()
            #         m.Notification(
            #             type_of=m.NotificationType.DISPUTE_CREATED.value,
            #             text=f"Dispute created for ticket {ticket.id} of user {seller_id}",
            #             user_id=seller_id,
            #         ).save()
            #     is_open = False if k == 1 else True
            #     room = m.Room(
            #         type_of=type_of,
            #         ticket_id=ticket.id,
            #         is_open=is_open,
            #         seller_id=seller_id,
            #         buyer_id=randint(1, NUM_TEST_USERS),
            #     ).save()
            #     for _ in range(5):
            #         m.Message(
            #             room_id=room.id,
            #             sender_id=randint(1, NUM_TEST_USERS),
            #             text=faker.text(max_nb_chars=200),
            #         ).save()
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
