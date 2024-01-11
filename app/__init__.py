import os

import sqlalchemy as sa

from flask import Flask, render_template, abort, request
from flask_login import LoginManager, current_user
from werkzeug.exceptions import HTTPException
from flask_migrate import Migrate
from flask_mail import Mail
from flask_sse import sse

from app.logger import log
from app.controllers import PagarmeClient
from .database import db

# instantiate extensions
login_manager = LoginManager()
migration = Migrate()
mail = Mail()
pagarme_client = PagarmeClient()


def create_app(environment="development") -> Flask:
    from config import config
    from app.views import (
        main_blueprint,
        auth_blueprint,
        user_blueprint,
        events_blueprint,
        tickets_blueprint,
        admin_blueprint,
        chat_auth_blueprint,
        chat_sell_blueprint,
        chat_buy_blueprint,
        pay_blueprint,
        chat_disputes_blueprint,
    )
    from app import models as m

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get("APP_ENV", environment)
    configuration = config(env)
    app.config.from_object(configuration)
    configuration.configure(app)
    log(log.INFO, "Configuration: [%s]", configuration.ENV)

    # Set up extensions.
    db.init_app(app)
    migration.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # init pagarme client
    pagarme_client.configure(configuration)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(tickets_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(chat_auth_blueprint)
    app.register_blueprint(chat_sell_blueprint)
    app.register_blueprint(chat_buy_blueprint)
    app.register_blueprint(pay_blueprint)
    app.register_blueprint(chat_disputes_blueprint)

    # SSE
    @sse.before_request
    def check_access():
        if not current_user.is_authenticated:
            abort(403)

        channel = request.args.get("channel")

        if not channel:
            abort(403)

        topic, identifier = channel.split(":")

        if topic == "room" and current_user.role != m.UserRole.admin.value:
            room = db.session.scalar(
                sa.select(m.Room).where(
                    sa.and_(
                        m.Room.unique_id == identifier,
                        sa.or_(m.Room.seller_id == current_user.id, m.Room.buyer_id == current_user.id),
                    )
                )
            )
            if not room:
                abort(403)

        elif topic == "notification" and current_user.uuid != identifier:
            abort(403)

    app.register_blueprint(sse, url_prefix="/sse")

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id: int) -> m.User | None:
        query = sa.select(m.User).where(m.User.id == int(id))
        return db.session.scalar(query)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = m.AnonymousUser

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code

    # Jinja globals
    from app.controllers.jinja_globals import (
        today,
        form_hidden_tag,
        date_from_datetime,
        time_delta,
        cut_seconds,
        card_mask,
        get_categories,
        get_chat_room_messages,
        get_chatbot_id,
        round_to_two_places,
        event_form_date,
    )

    app.jinja_env.globals["today"] = today
    app.jinja_env.globals["form_hidden_tag"] = form_hidden_tag
    app.jinja_env.globals["date_from_datetime"] = date_from_datetime
    app.jinja_env.globals["event_form_date"] = event_form_date
    app.jinja_env.globals["time_delta"] = time_delta
    app.jinja_env.globals["cut_seconds"] = cut_seconds
    app.jinja_env.globals["card_mask"] = card_mask
    app.jinja_env.globals["get_categories"] = get_categories
    app.jinja_env.globals["get_chat_room_messages"] = get_chat_room_messages
    app.jinja_env.globals["get_chatbot_id"] = get_chatbot_id
    app.jinja_env.globals["round_to_two_places"] = round_to_two_places

    return app
