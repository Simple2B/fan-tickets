from random import randint
from faker import Faker
from app import db
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
    "Concert",
    "Festival",
    "Theater",
    "Cinema",
    "Party",
    "Conference",
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
        activated = True if i - num_objects == 3 else False
        user = m.User(
            username=f"{first_name}{last_name}{randint(10, 99)}",
            email=email,
            role=role.value,
            password="pass",
            activated=activated,
        )
        db.session.add(user)
        log(log.INFO, "User generated: [%s]", user)
    db.session.commit()
    users_number = m.User.count()
    log(log.INFO, "[%d] users generated", users_number)


def generate_test_events(num_objects: int = NUM_TEST_EVENTS):
    for location_name in TEST_LOCATIONS:
        m.Location(
            name=location_name,
        ).save()
    for category_name in TEST_CATEGORIES:
        m.Category(
            name=category_name,
        ).save()
    for i in range(NUM_TEST_EVENTS):
        event = m.Event(
            name=f"Event {i}",
            observations=faker.text(max_nb_chars=200),
            location_id=randint(1, len(TEST_LOCATIONS)),
            category_id=randint(1, len(TEST_CATEGORIES)),
            date_time=faker.date_time_between(start_date="-3m", end_date="+3m"),
        ).save()
        for j in range(12):
            price_net = randint(10, 1000)
            price_gross = price_net * 1.08
            is_in_cart = True if j <= 1 else False
            is_reserved = True if 2 <= j <= 4 else False
            is_sold = True if 5 <= j <= 7 else False
            seller_id = randint(1, NUM_TEST_USERS)
            buyer_id = randint(1, NUM_TEST_USERS)
            ticket = m.Ticket(
                event_id=event.id,
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
            ).save()
            m.Notification(
                type_of=m.NotificationType.TICKET_PUBLISHED.value,
                text=f"Dispute created for ticket {ticket.id} of user {seller_id}",
                user_id=seller_id,
            ).save()
            if is_sold:
                m.Notification(
                    type_of=m.NotificationType.TICKET_SOLD.value,
                    text=f"Ticket {ticket.id} of user {seller_id} is sold",
                    user_id=seller_id,
                ).save()
            if ticket.is_available:
                m.Notification(
                    type_of=m.NotificationType.TICKET_AVAILABLE.value,
                    text=f"Ticket {ticket} is available",
                    user_id=seller_id,
                ).save()
            for k in range(4):
                type_of = m.RoomType.DISPUTE.value if k == 0 else m.RoomType.CHAT.value
                if type_of == m.RoomType.DISPUTE.value:
                    m.Dispute(
                        description=faker.text(max_nb_chars=200),
                        is_active=True,
                        buyer_id=buyer_id,
                        ticket_id=ticket.id,
                    ).save()
                    m.Notification(
                        type_of=m.NotificationType.DISPUTE_CREATED.value,
                        text=f"Dispute created for ticket {ticket.id} of user {seller_id}",
                        user_id=seller_id,
                    ).save()
                is_open = False if k == 1 else True
                room = m.Room(
                    type_of=type_of,
                    ticket_id=ticket.id,
                    is_open=is_open,
                ).save()
                for _ in range(5):
                    m.Message(
                        room_id=room.id,
                        sender_id=randint(1, NUM_TEST_USERS),
                        text=faker.text(max_nb_chars=200),
                    ).save()


def populate(count: int = NUM_TEST_USERS):
    generate_test_users()
    generate_test_events()
