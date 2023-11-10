import os
import tomllib
from functools import lru_cache
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

    # Super admin
    ADMIN_USERNAME: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    # Pagination
    DEFAULT_PAGE_SIZE: int
    PAGE_LINKS_NUMBER: int

    # API
    IS_API: bool = False
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @staticmethod
    def configure(app: Flask):
        # Implement this method to do further configuration on your app.
        pass

    # `.env` takes priority over `project.env`
    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    ALCHEMICAL_DATABASE_URL: str = "sqlite:///" + os.path.join(
        BASE_DIR, "database-dev.sqlite3"
    )

    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING: bool = True
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = False
    ALCHEMICAL_DATABASE_URL: str = "sqlite:///" + os.path.join(
        BASE_DIR, "database-test.sqlite3"
    )

    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


class ProductionConfig(BaseConfig):
    """Production configuration."""

    ALCHEMICAL_DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED: bool = True

    model_config = SettingsConfigDict(extra="allow", env_file=("project.env", ".env"))


@lru_cache
def config(name=APP_ENV) -> DevelopmentConfig | TestingConfig | ProductionConfig:
    CONF_MAP = dict(
        development=DevelopmentConfig(),
        testing=TestingConfig(),
        production=ProductionConfig(),
    )
    configuration = CONF_MAP[name]
    configuration.ENV = name
    return configuration
