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
        ).save()
        print("admin created")

    @app.cli.command("print-users")
    def print_users():
        print(m.User.all())

    @app.cli.command("set-users-images")
    def set_users_images():
        from test_flask.db import set_users_images

        set_users_images()

        print("users images are set")

    @app.cli.command("get-buyers")
    def get_buyers():
        sold_tickets_query = m.Ticket.select().where(m.Ticket.is_sold.is_(True))
        sold_tickets = db.session.scalars(sold_tickets_query).all()
        for ticket in sold_tickets:
            print(ticket.buyer.username)
