import click
from flask import Flask
import sqlalchemy as sa
from sqlalchemy import orm
from app import models as m
from app import db, forms
from app import schema as s


def init(app: Flask):
    # flask cli context setup
    @app.shell_context_processor
    def get_context():
        """Objects exposed here will be automatically available from the shell."""
        return dict(app=app, db=db, m=m, f=forms, s=s, sa=sa, orm=orm)

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
        query = m.User.select().where(m.User.email == app.config["ADMIN_EMAIL"])
        if db.session.execute(query).first():
            print(f"User with e-mail: [{app.config['ADMIN_EMAIL']}] already exists")
            return
        m.User(
            username=app.config["ADMIN_USERNAME"],
            email=app.config["ADMIN_EMAIL"],
            phone="+380000000000",
            card="0000000000000000",
            password=app.config["ADMIN_PASSWORD"],
            activated=True,
            role=m.UserRole.admin.value,
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
        user.save()

        print(user.subscribed_events)

    @app.cli.command("delete-users")
    @click.option("--email", type=str)
    def delete_user(email: str):
        """
        Command for deleting user
        """
        user_query = m.User.select().where(m.User.email == email)
        users = db.session.scalars(user_query).all()
        if not users:
            print(f"User with e-mail: [{email}] not found")
            return
        for user in users:
            messages_query = m.Message.select().where(m.Message.sender_id == user.id)
            messages = db.session.scalars(messages_query).all()
            for message in messages:
                db.session.delete(message)
            rooms_query = m.Room.select().where(sa.or_(m.Room.seller_id == user.id, m.Room.buyer_id == user.id))
            rooms = db.session.scalars(rooms_query).all()
            for room in rooms:
                db.session.delete(room)
            db.session.delete(user)
            db.session.commit()
            print(f"User {user.username} deleted")

    @app.cli.command("all-users")
    def all_users():
        """
        Command for getting all users
        """
        users_query = m.User.select()
        users = db.session.scalars(users_query).all()
        print(users)
