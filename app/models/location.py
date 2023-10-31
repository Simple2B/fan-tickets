from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin, gen_uuid


class Location(db.Model, ModelMixin):
    """
    Model for events' locations.

    Routes:
    - POST /admin/locations/create (admin)
    - GET /admin/locations (admin)
    - GET /admin/locations/{location_unique_id} (admin)
    - GET /admin/locations/nearby/{coordinates} (admin, ajax sort)
    - GET /admin/locations/by_event/{event_unique_id} (admin, ajax sort)
    - PUT /admin/locations/update/{location_unique_id} (admin)
    - DELETE /admin/locations/delete/{location_unique_id} (admin)

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
    # TODO: add image
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
