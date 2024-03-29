from datetime import datetime, timedelta
from random import randint
from faker import Faker
from sqlalchemy import orm
from app import models as m
from app.controllers.notification_client import NotificationType


NUM_TEST_USERS = 30
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
    "Concert",
    "Festival",
    "Theater",
    "Cinema",
    "Party",
    "Conference",
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

fake = Faker()


def generate_test_users(session: orm.Session, num_objects: int = NUM_TEST_USERS):
    DOMAINS = ("com", "com.br", "net", "net.br", "org", "org.br", "gov", "gov.br")

    for i in range(num_objects):
        first_name = fake.first_name()
        last_name = fake.last_name()
        company = fake.company().split()[0].strip(",")
        dns_org = fake.random_choices(elements=DOMAINS, length=1)[0]
        email = f"{first_name.lower()}.{last_name.lower()}@{company.lower()}.{dns_org}"
        role = m.UserRole.admin if i < 3 else m.UserRole.client
        activated = True if i - num_objects == 3 else False
        user = m.User(
            username=f"{first_name}{last_name}{randint(10, 99)}",
            email=email,
            role=role.value,
            password="pass",
            activated=activated,
        )
        session.add(user)
    session.commit()


def generate_test_events(
    session: orm.Session,
):
    locations: list[m.Location] = []
    for location_name in TEST_LOCATIONS:
        location = m.Location(
            name=location_name,
        )
        session.add(location)
        locations.append(location)
        # session.commit()
    categories: list[m.Category] = []
    for category_name in TEST_CATEGORIES:
        category = m.Category(
            name=category_name,
        )
        session.add(category)
        categories.append(category)
        # session.commit()
    for i in range(NUM_TEST_EVENTS):
        location_id = randint(1, len(TEST_LOCATIONS))
        location_name = locations[location_id - 1].name
        category_id = randint(1, len(TEST_CATEGORIES))
        category_name = categories[category_id - 1].name
        seller_id = randint(1, NUM_TEST_USERS)
        event = m.Event(
            name=f"{location_name} {category_name} {i}",
            url=f"https://{location_name.lower().replace(' ', '-')}-{category_name.lower().replace(' ', '-')}-{i}.com",
            observations=fake.text(max_nb_chars=200),
            warning="don't forget to bring your ID",
            location_id=location_id,
            category_id=category_id,
            creator_id=seller_id,
            date_time=datetime.now() + timedelta(days=randint(-10, 100)),
        )
        session.add(event)
        session.flush()
        for j in range(12):
            price_net = randint(10, 1000)
            price_gross = price_net * 1.08
            is_in_cart = True if j <= 1 else False
            is_reserved = True if 2 <= j <= 4 else False
            is_sold = True if 5 <= j <= 7 else False
            buyer_id = randint(1, NUM_TEST_USERS)
            ticket = m.Ticket(
                event_id=event.id,
                description=fake.text(max_nb_chars=200),
                ticket_type=TEST_TICKET_TYPES[randint(0, 2)],
                ticket_category=TEST_TICKET_CATEGORIES[randint(0, 2)],
                warning=fake.text(max_nb_chars=200),
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
            )
            session.add(ticket)
            session.flush()
            notification = m.Notification(
                type_of=NotificationType.TICKET_PUBLISHED.value,
                text=f"Dispute created for ticket {ticket.id} of user {seller_id}",
                user_id=seller_id,
            )
            session.add(notification)
            if is_sold:
                notification = m.Notification(
                    type_of=NotificationType.TICKET_SOLD.value,
                    text=f"Ticket {ticket.id} of user {seller_id} is sold",
                    user_id=seller_id,
                )
                session.add(notification)
            if ticket.is_available:
                notification = m.Notification(
                    type_of=NotificationType.TICKET_AVAILABLE.value,
                    text=f"Ticket {ticket} is available",
                    user_id=seller_id,
                )
                session.add(notification)
            for k in range(4):
                type_of = m.RoomType.DISPUTE.value if k == 0 else m.RoomType.CHAT.value
                if type_of == m.RoomType.DISPUTE.value:
                    notification = m.Notification(
                        type_of=NotificationType.DISPUTE_CREATED.value,
                        text=f"Dispute created for ticket {ticket.id} of user {seller_id}",
                        user_id=seller_id,
                    )
                    session.add(notification)
                is_open = False if k == 1 else True
                room = m.Room(
                    type_of=type_of,
                    ticket_id=ticket.id,
                    is_open=is_open,
                    seller_id=seller_id,
                    buyer_id=randint(1, NUM_TEST_USERS),
                )
                session.add(room)
                session.flush()
                for _ in range(5):
                    message = m.Message(
                        room_id=room.id,
                        sender_id=randint(1, NUM_TEST_USERS),
                        text=fake.text(max_nb_chars=200),
                    )
                    session.add(message)
