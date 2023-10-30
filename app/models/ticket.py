from enum import Enum


from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin




if TYPE_CHECKING:
    # from .user import User
    # from .category import Category
    # from .location import Location
    
    
class TicketType(Enum):
    TRACK = "track"
    BOX = "box"
    BACK_STAGE = "back_stage"



class Ticket(db.Model, ModelMixin):
    """
    Model for events

    Actions in admin section:
    - create
    - read
    - update
    - delete
    - set a foreign key from events to locations
    - set a foreign key from events to categories
    - set a foreign key from tickets to events

    - quantity, original value, sales value
    - observations/conditions
    - read ticket barcode / QRcode
    - insert warning
    - net amount (price)
    - the amount the buyer should pay
    """

    __tablename__ = "tickets"






    description: orm.Mapped[str] = orm.mapped_column(
        sa.String(512),
        unique=False,
        nullable=False,
    )
    
    
    
    
    
    
    ticket_type: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), default=TicketType.TRACK.value
    )