from datetime import datetime, timedelta
import click
from flask import Flask
import sqlalchemy as sa
from sqlalchemy import or_, orm
from app import models as m
from app import db, forms, pagarme_client
from app import schema as s


def init(app: Flask):
    # flask cli context setup
    @app.shell_context_processor
    def get_context():
        """Objects exposed here will be automatically available from the shell."""
        return dict(app=app, db=db, m=m, f=forms, s=s, sa=sa, orm=orm, pagarme_client=pagarme_client)

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
            sa.select(m.User.username)
            .select_from(sa.join(m.Ticket, m.User, m.Ticket.buyer_id == m.User.id))
            .where(m.Ticket.is_sold.is_(True))
            .group_by(m.User.username)
            .order_by(m.User.username)
        )
        sold_tickets_buyers = db.session.scalars(sold_tickets_query).all()
        print(sold_tickets_buyers)

    @app.cli.command("set-subscriptions")
    @click.option("--username", type=str)
    def set_subscriptions(username: str):
        """
        Command for setting testing subscriptions to display in profile
        """
        user_query = m.User.select().where(m.User.username == username)
        user = db.session.scalar(user_query)
        events_query = m.Event.select().limit(3)
        events = db.session.scalars(events_query).all()

        print(user)

        user.subscribed_events.extend(events)
        user.password = "pass"
        user.save()

        print(user.subscribed_events)

    @app.cli.command("delete-users")
    @click.option("--email", type=str)
    def delete_user(email: str):
        user_query = m.User.select().where(m.User.email == email)
        user: m.User = db.session.scalar(user_query)
        if not user:
            print(f"User with e-mail: [{email}] not found")
            return
        rooms_query = m.Room.select().where(sa.or_(m.Room.seller_id == user.id, m.Room.buyer_id == user.id))
        rooms: m.Room = db.session.scalars(rooms_query).all()
        messages_query = (
            m.Message.select()
            .join(m.Room, m.Message.room_id == m.Room.id)
            .where(or_(m.Message.sender_id == user.id, m.Room.seller_id == user.id, m.Room.buyer_id == user.id))
        )
        messages = db.session.scalars(messages_query).all()
        for message in messages:
            db.session.delete(message)
        for room in rooms:
            db.session.delete(room)
        notifications_query = m.Notification.select().where(m.Notification.user_id == user.id)
        notifications = db.session.scalars(notifications_query).all()
        print("notifications", notifications)
        if notifications:
            for notification in notifications:
                db.session.delete(notification)
        notification_configs_query = m.NotificationsConfig.select().where(m.NotificationsConfig.user_id == user.id)
        notification_configs = db.session.scalars(notification_configs_query).all()
        for notification_config in notification_configs:
            db.session.delete(notification_config)
        payments_query = m.Payment.select().where(m.Payment.buyer_id == user.id)
        payments = db.session.scalars(payments_query).all()
        if payments:
            for payment in payments:
                db.session.delete(payment)
        db.session.delete(user)
        db.session.commit()
        print(f"User {user.email} deleted")

    @app.cli.command("all-users")
    def all_users():
        """
        Command for getting all users
        """
        users_query = m.User.select()
        users = db.session.scalars(users_query).all()
        for user in users:
            print(user.id, user.email, user.role, user.tickets_bought)

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
        print("rollbacked")

    @app.cli.command("create-pagarme-order")
    def create_pagarme_order():
        """Create test pagarme order"""

        with open("test_flask/assets/pagarme/create_order_pix.json") as json_f:
            json_data = json_f.read()
            data = s.PagarmeCreateOrderPix.model_validate_json(json_data)

        resp = pagarme_client.create_order_pix(data)
        print(resp)
