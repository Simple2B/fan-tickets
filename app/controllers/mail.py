from typing import Iterable

from flask import Flask
from flask_mail import Mail, Message

from app import models as m


class MailController:
    mail: Mail
    sender_email: str

    def init_app(self, app: Flask):
        self.mail = Mail()
        self.mail.init_app(app)
        self.sender_email = app.config["MAIL_DEFAULT_SENDER"]

    def send_email(self, users: Iterable[m.User], subject: str, body: str):
        msg = Message(
            subject=subject,
            sender=self.sender_email,
            recipients=[user.email for user in users],
        )

        msg.html = body
        self.mail.send(msg)
