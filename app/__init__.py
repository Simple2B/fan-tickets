import os

from flask import Flask, render_template
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from flask_migrate import Migrate
from flask_mail import Mail

from app.logger import log
from .database import db

# instantiate extensions
login_manager = LoginManager()
migration = Migrate()
mail = Mail()


def create_app(environment="development") -> Flask:
    from config import config
    from app.views import (
        main_blueprint,
        auth_blueprint,
        user_blueprint,
        events_blueprint,
        tickets_blueprint,
        admin_blueprint,
        chat_blueprint,
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

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(tickets_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(chat_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id: int):
        query = m.User.select().where(m.User.id == int(id))
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
        form_hidden_tag,
        date_from_datetime,
        time_delta,
        cut_seconds,
        card_mask,
        get_categories,
    )

    app.jinja_env.globals["form_hidden_tag"] = form_hidden_tag
    app.jinja_env.globals["date_from_datetime"] = date_from_datetime
    app.jinja_env.globals["time_delta"] = time_delta
    app.jinja_env.globals["cut_seconds"] = cut_seconds
    app.jinja_env.globals["card_mask"] = card_mask
    app.jinja_env.globals["get_categories"] = get_categories

    return app
