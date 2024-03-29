from datetime import datetime, timedelta
import click
from flask import Flask
import sqlalchemy as sa
from app import models as m
from app import schema as s
from app import flask_sse_notification, pagarme_client
from app.database import db
from app.controllers.notification_client import NotificationType
from config import config


CFG = config()


def init_shell_commands(app: Flask):
    @app.cli.command()
    @click.option("--count", default=100, type=int)
    def db_populate(count: int):
        """Fill DB by dummy data."""
        from test_flask.db import populate

        populate(count)
        print(f"DB populated by {count} instancies")

    @app.cli.command("create-admin")
    def create_admin():
        """Create super admin account"""
        with open("app/static/img/default_avatar.png", "rb") as f:
            picture: m.Picture = m.Picture(
                filename="default_avatar",
                file=f.read(),
            ).save()
        with open("app/static/img/default_passport.png", "rb") as f:
            document: m.Picture = m.Picture(
                filename="default_passport",
                file=f.read(),
            ).save(False)
        query = m.User.select().where(m.User.email == app.config["ADMIN_EMAIL"])
        if db.session.execute(query).first():
            print(f"User with e-mail: [{app.config['ADMIN_EMAIL']}] already exists")
            return
        m.GlobalFeeSettings().save(False)
        m.User(
            username=app.config["ADMIN_USERNAME"],
            name=app.config["ADMIN_NAME"],
            last_name=app.config["ADMIN_LAST_NAME"],
            email=app.config["ADMIN_EMAIL"],
            phone="+380000000000",
            card="0000000000000000",
            password=app.config["ADMIN_PASSWORD"],
            activated=True,
            role=m.UserRole.admin.value,
            picture_id=picture.id,
            identity_document=document,
            birth_date=datetime.now() - timedelta(days=365 * 20),
        ).save()
        print("admin created")

    @app.cli.command("print-users")
    def print_users():
        print(m.User.all())

    @app.cli.command("set-users-images")
    def set_users_images():
        """
        This command sets images for users if we need to see them in the profile
        """
        from test_flask.db import set_users_images

        set_users_images()

        print("users images are set")

    @app.cli.command("get-buyers")
    def get_buyers():
        """
        This command has to show all users who bought tickets
        To make us available add testing subscriptions if it's needed
        """
        sold_tickets_query = (
            sa.select(m.User.email)
            .select_from(sa.join(m.Ticket, m.User, m.Ticket.buyer_id == m.User.id))
            .where(m.Ticket.is_sold.is_(True))
            .group_by(m.User.email)
            .order_by(m.User.email)
        )
        sold_tickets_buyers = db.session.scalars(sold_tickets_query).all()
        print(sold_tickets_buyers)

    @app.cli.command("set-subscriptions")
    @click.option("--email", type=str)
    def set_subscriptions(email: str):
        """
        Command for setting testing subscriptions to display in profile
        """
        event = db.session.scalar(sa.select(m.Event))
        user: m.User = db.session.scalar(
            m.User.select().where(m.User.email == email, m.User.subscribed_events.any(m.Event.id == event.id))
        )

        if not user:
            user = db.session.scalar(m.User.select().where(m.User.email == email))
            if not user:
                print(f"User with e-mail: [{email}] not found")
                return
            user.subscribed_events.append(event)

        seller = db.session.scalar(m.User.select().where(m.User.role == m.UserRole.client.value, m.User.id != user.id))

        for i in range(3):
            ticket = m.Ticket(
                event=event,
                seller=seller,
                buyer=user,
                is_sold=True,
            )
            payment = m.Payment(
                ticket=ticket,
                buyer=user,
            )
            db.session.add(payment)
        user.password = "pass"
        db.session.commit()

    @app.cli.command("delete-user")
    @click.option("--email", type=str)
    def delete_user(email: str):
        user_query = m.User.select().where(m.User.email == email)
        user: m.User = db.session.scalar(user_query)
        if not user:
            print(f"User with e-mail: [{email}] not found")
            return

        user.activated = False
        user.is_deleted = True
        user.email = f"{user.email}_deleted_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        user.username = f"{user.username}_d"
        user.phone = f"{user.phone}-d"
        user.save()
        print(f"User {user.email} deleted")

    @app.cli.command("all-users")
    def all_users():
        """
        Command for getting all users
        """
        users_query = m.User.select()
        users = db.session.scalars(users_query).all()
        for user in users:
            print(user.id, user.email, user.role, user.username, user.name, user.last_name)

    @app.cli.command("reassign-events")
    @click.option("--username", type=str)
    def reassign_events(username: str):
        """
        Command for reassigning events to another user
        """
        user_query = m.User.select().where(m.User.username == username)
        user: m.User = db.session.scalar(user_query)
        if not user:
            print(f"User with username: [{username}] not found")
            return
        events = db.session.scalars(m.Event.select()).all()
        for event in events[:6]:
            event.creator_id = user.id
            event.approved = True
            event.save()
        print(f"Events of user {user.username} reassigned")

    @app.cli.command("rollback")
    def rollback():
        """
        Command for rollbacking all changes
        """
        db.session.rollback()

    @app.cli.command("send-admin-notification")
    def send_admin_notification():
        flask_sse_notification.notify_admin({"username": "aa"}, db.session, NotificationType.NEW_REGISTRATION)

    @app.cli.command("set-test-notifications")
    @click.option("--login")
    def set_test_notifications(login):
        if not login:
            user = db.session.scalar(sa.select(m.User).where(m.User.role == m.UserRole.admin.value))
        else:
            user = db.session.scalar(sa.select(m.User).where(m.User.username == login))

        if not user:
            print("User not found")
            return

        print(f"Setting user notifications [{user}]")
        notifications = db.session.scalars(user.notifications.select().order_by(m.Notification.created_at.desc()))

        for i, notification in enumerate(notifications):
            notification.payload = {"test": f"test_{i}"}

        db.session.commit()
        notifications_count = db.session.scalar(
            sa.select(sa.func.count(m.Notification.id)).where(m.Notification.users.any(m.User.id == user.id))
        )
        print(f"Notifications set: {notifications_count}")
        print("rollbacked")

    @app.cli.command("create-pagarme-order")
    def create_pagarme_order():
        """Create test pagarme order"""

        with open("test_flask/assets/pagarme/create_order_pix.json") as json_f:
            json_data = json_f.read()
            data = s.PagarmeCreateOrderPix.model_validate_json(json_data)

        resp = pagarme_client.create_order_pix(data)
        print(resp)

    @app.cli.command("reserve")
    def reserve():
        """Reserve tickets for testing"""
        tickets_query = m.Ticket.select()
        tickets = db.session.scalars(tickets_query).all()

        reserved_tickets = []
        for i, ticket in enumerate(tickets):
            if i % 3 == 0:
                ticket.is_reserved = True
                ticket.last_reservation_time = datetime.now() - timedelta(minutes=31)
                ticket.save(False)
                reserved_tickets.append(ticket)
        db.session.commit()

        print(reserved_tickets)

    @app.cli.command("unreserve")
    def unreserve():
        """Unreserve all tickets"""
        tickets_query = (
            m.Ticket.select()
            .where(m.Ticket.is_reserved.is_(True), m.Ticket.is_deleted.is_(False), m.Ticket.is_sold.is_(False))
            .where(m.Ticket.last_reservation_time < datetime.now() - timedelta(minutes=CFG.TICKETS_IN_CART_EXPIRES_IN))
            # .where(m.Ticket.event.has(m.Event.location.has(m.Location.name.ilike("%Rio%"))))
        )
        tickets: list[m.Ticket] = db.session.scalars(tickets_query).all()

        if tickets:
            for ticket in tickets:
                ticket.is_reserved = False
                ticket.last_reservation_time = datetime.now()
                ticket.save()
                print(ticket, "unreserved")
            print(len(tickets), "with expired reservation unreserved")

        else:
            print("No tickets to unreserve")

    @app.cli.command("delete-tickets")
    @click.option("--location", type=str)
    def delete_tickets(location: str):
        """Delete all tickets"""
        tickets_query = m.Ticket.select().where(
            m.Ticket.event.has(m.Event.location.has(m.Location.name.ilike(f"%{location}%")))
        )
        tickets = db.session.scalars(tickets_query).all()
        for ticket in tickets:
            payments_query = m.Payment.select().where(m.Payment.ticket_id == ticket.id)
            payments = db.session.scalars(payments_query).all()
            if payments:
                for payment in payments:
                    db.session.delete(payment)
            db.session.delete(ticket)
        db.session.commit()
        print("Selected tickets deleted")

    @app.cli.command("create-unpaid-tickets")
    def create_unpaid_tickets():
        """Create test unpaid tickets"""
        events_query = m.Event.select().where(m.Event.date_time < datetime.now())
        events = db.session.scalars(events_query).all()
        assert events

        TESTING_TICKETS_TO_PAY_PER_EVENT = 5

        tickets_to_pay: list[m.Ticket] = []
        for event in events:
            for i in range(TESTING_TICKETS_TO_PAY_PER_EVENT):
                ticket = m.Ticket(
                    seller_id=event.creator_id,
                    buyer_id=1,
                    event=event,
                    is_sold=True,
                    last_reservation_time=datetime.now() - timedelta(hours=49),
                    price_net=100,
                    price_gross=111,
                ).save()
                tickets_to_pay.append(ticket)
        print(len(tickets_to_pay), "tickets unpaid to sellers created")

    @app.cli.command("get-unpaid-tickets")
    def get_unpaid_tickets():
        """
        Testing command to get unpaid tickets
        """
        tickets_query = m.Ticket.select().where(
            m.Ticket.is_sold.is_(True),
            m.Ticket.paid_to_seller_at.is_(None),
            m.Ticket.is_deleted.is_(True),
        )
        tickets: list[m.Ticket] = db.session.scalars(tickets_query).all()
        for ticket in tickets:
            last_reservation_time = (
                ticket.last_reservation_time.strftime("%Y-%m-%d %H:%M:%S") if ticket.last_reservation_time else None
            )
            reserved_from_now = datetime.now() - ticket.last_reservation_time if ticket.last_reservation_time else None
            print(
                "Paid:",
                ticket.paid_to_seller_at,
                "Deleted:",
                ticket.is_deleted,
                "Reserved:",
                last_reservation_time,
                "Reserved from now:",
                reserved_from_now,
                "Seller:",
                ticket.seller.email,
                "Buyer:",
                ticket.buyer.email,
            )

        print(len(tickets), "tickets unpaid to sellers")

    @app.cli.command("pay-sellers")
    def pay_sellers():
        """
        Pays for sold tickets to sellers
        after 48 hours if no disputes were started
        """
        tickets_query = m.Ticket.select().where(
            m.Ticket.is_sold.is_(True),
            m.Ticket.last_reservation_time < datetime.now() - timedelta(days=2),
            m.Ticket.is_deleted.is_(False),
        )
        tickets: list[m.Ticket] = db.session.scalars(tickets_query).all()

        if tickets:
            print(len(tickets), "tickets to pay")
            for ticket in tickets:
                print(f"Ticket {ticket.unique_id} sold at {ticket.last_reservation_time} is ready to pay")

                disputes = [room for room in ticket.rooms if room.type_of == m.RoomType.DISPUTE.value]

                if disputes:
                    print(f"Ticket {ticket.unique_id} has disputes")
                    continue

                if not ticket.seller.recipient_id:
                    recipient_credentials = pagarme_client.check_recipient_credentials(ticket.seller)
                    if not recipient_credentials:
                        # TODO: user notification to fill out the recipient credentials
                        print(
                            f"Ticket {ticket.unique_id} is not paid. Recipient credentials for {ticket.seller.email} not found"
                        )
                        continue

                    # forming data for creating a recipient
                    recipient_data = pagarme_client.prepare_recipient_data(ticket)

                    # going to pagar to create a new recipient
                    # if success saving a recipient_id to the seller
                    recipient_id = pagarme_client.create_recipient(recipient_data, ticket.seller)
                    if not recipient_id:
                        print(f"Pagarme error. Recipient for {ticket.seller.email} not created")
                        continue

                # forming data for split payment
                split_data = pagarme_client.generate_split_data(ticket)
                if not split_data:
                    continue

                response = pagarme_client.create_split(split_data)  # pays to seller via pagarme

                if response:
                    ticket.paid_to_seller_at = datetime.now()
                    ticket.is_deleted = True
                    print(
                        f"Ticket {ticket.unique_id} paid to seller [{ticket.seller.email}] at {ticket.paid_to_seller_at}"
                    )
                else:
                    print(f"Ticket {ticket.unique_id} is not paid")
            print(len(tickets), "paid to sellers")
            db.session.commit()
        else:
            print("No tickets to pay")

    def obsolete_rooms():
        rooms_query = m.Room.select().where(
            sa.or_(m.Room.seller_id.is_(None), m.Room.buyer_id.is_(None)),
            m.Room.created_at < datetime.now() - timedelta(days=2),
        )
        rooms: list[m.Room] = db.session.scalars(rooms_query).all()
        return rooms

    @app.cli.command("delete-rooms")
    def delete_rooms():
        """
        Deletes rooms if last message was sent more than 48 hours ago
        """

        rooms: list[m.Room] = obsolete_rooms()
        print(len(rooms), "rooms to delete")
        for room in rooms:
            messages_query = m.Message.select().where(m.Message.room_id == room.id)
            messages = db.session.scalars(messages_query).all()
            for message in messages:
                db.session.delete(message)
            print(room, "to delete")
            db.session.delete(room)
            db.session.commit()

        rooms_left: list[m.Room] = obsolete_rooms()

        print(len(rooms_left), "rooms left")

    @app.cli.command("untransfer")
    @click.option("--email", type=str)
    def untransfer(email: str):
        """
        Command for testing untransferring tickets
        """
        user_query = m.User.select().where(m.User.email == email)
        user: m.User = db.session.scalar(user_query)

        tickets_query = m.Ticket.select().where(m.Ticket.buyer_id == user.id)
        tickets: list[m.Ticket] = db.session.scalars(tickets_query).all()
        for ticket in tickets:
            ticket.is_transferred = False
            ticket.save()
            print(ticket, "untransferred")
