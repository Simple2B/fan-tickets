import os
import tomllib
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from flask import Flask

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ENV = os.environ.get("APP_ENV", "development")


def get_version() -> str:
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)["tool"]["poetry"]["version"]


class BaseConfig(BaseSettings):
    """Base configuration."""

    ENV: str = "base"
    APP_NAME: str = "Fan Ticket"
    VERSION: str = get_version()
    SECRET_KEY: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    WTF_CSRF_ENABLED: bool = False

    # Mail config
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USE_TLS: bool
    MAIL_USE_SSL: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_DEFAULT_SENDER: str

    # Twilio
    TWILIO_ACCOUNT_SID: str = "some_twilio_account_sid"
    TWILIO_AUTH_TOKEN: str = "some_twilio_auth_token"
    TWILIO_PHONE_NUMBER: str = "some_twilio_phone_number"

    # Super admin
    ADMIN_USERNAME: str
    ADMIN_NAME: str = "Admin_name"
    ADMIN_LAST_NAME: str = "Admin_last_name"
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    # Pagination
    DEFAULT_PAGE_SIZE: int
    PAGE_LINKS_NUMBER: int
    EVENTS_PER_PAGE: int
    TICKETS_PER_PAGE: int = 10
    TICKETS_PER_CHAT: int = 3

    # UI config
    DATE_PICKER_FORMAT: str = "%m/%d/%Y"
    DATE_PLATFORM_FORMAT: str = "%d %b %Y"
    DATE_CHAT_HISTORY_FORMAT: str = "%m/%d/%Y %H:%M"
    PATTERN_EMAIL: str = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    PATTERN_PHONE: str = r"^\+?\d{10,13}$"

    # API
    IS_API: bool = False
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    IMAGE_MAX_WIDTH: int = 512

    # User's form
    USER_USERNAME_MIN_LENGTH: int = 3
    USER_USERNAME_MAX_LENGTH: int = 30
    USER_PHONE_MIN_LENGTH: int = 7
    USER_PHONE_MAX_LENGTH: int = 16
    USER_CARD_LENGTH: int = 16
    USER_PASSWORD_MIN_LENGTH: int = 6
    USER_PASSWORD_MAX_LENGTH: int = 30

    # Chat registration default values
    CHAT_DEFAULT_USERNAME: str = "guest"
    CHAT_DEFAULT_BOT_ID: int = 2
    CHAT_DEFAULT_BOT_USERNAME: str = "FanTicket"
    CHAT_DEFAULT_EMAIL: str = "empty@email.com"
    CHAT_DEFAULT_PHONE: str = "+3800000000000"
    CHAT_DEFAULT_CARD: str = "0000000000000000"

    # dev base url
    DEV_BASE_URL: str = "127.0.0.1:5000/"
    STAGING_BASE_URL: str = "https://fan-ticket.simple2b.org/"

    # platform commission rate
    PLATFORM_COMMISSION_RATE: float = 1.08

    # pagar.me
    PAGARME_BASE_URL: str = "https://api.pagar.me/core/v5/"
    PAGARME_WEBHOOK_URL: str = "http://localhost:8080/pay/webhook"
    PAGARME_CONNECTION: bool = False
    PAGARME_SECRET_KEY: str | None = None
    PAGARME_CHECKOUT_EXPIRES_IN: int = 30  # minutes
    PAGARME_DEFAULT_PAYMENT_METHOD: str = "credit_card"
    BRASIL_COUNTRY_PHONE_CODE: str = "55"
    BRASIL_COUNTRY_AREA_CODE: str = "11"

    # Redis
    REDIS_URL: str

    @staticmethod
    def configure(app: Flask):
        # Implement this method to do further configuration on your app.
        pass

    # `.env` takes priority over `project.env`
    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    ALCHEMICAL_DATABASE_URL: str = Field(
        alias="DEVEL_DATABASE_URL",
        default="sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3"),
    )
    REDIS_URL: str = Field(
        alias="REDIS_URL_LOCAL",
    )

    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING: bool = True
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = False
    ALCHEMICAL_DATABASE_URL: str = "sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3")

    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


class ProductionConfig(BaseConfig):
    """Production configuration."""

    ALCHEMICAL_DATABASE_URL: str = Field(
        alias="DATABASE_URL",
        default="sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3"),
    )
    WTF_CSRF_ENABLED: bool = True

    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


@lru_cache
def config(name=APP_ENV) -> DevelopmentConfig | TestingConfig | ProductionConfig:
    CONF_MAP = dict(
        development=DevelopmentConfig,
        testing=TestingConfig,
        production=ProductionConfig,
    )
    configuration = CONF_MAP[name]()
    configuration.ENV = name
    return configuration
