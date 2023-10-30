from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .ticket import Ticket
    from .message import Message


class Rate(db.Model, ModelMixin):
    """
    Model for sellers' rates
    """
