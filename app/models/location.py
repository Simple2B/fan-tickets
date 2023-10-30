from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


class Location(db.Model, ModelMixin):
    """
    Model for events' locations.

    Routes:
    - POST /locations/create
    - GET /locations
    - GET /locations/{location_unique_id}
    - GET /locations/nearby/{coordinates}
    - GET /locations/by_event/{event_unique_id}
    - PUT /locations/update/{location_unique_id}
    - DELETE /locations/delete/{location_unique_id}

    """

    __tablename__ = "locations"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        nullable=False,
    )
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_uuid,
    )
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
