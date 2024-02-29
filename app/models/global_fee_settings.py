import sqlalchemy as sa
from enum import Enum
from sqlalchemy import orm
from .utils import ModelMixin
from app.database import db


class TicketsSortingType(Enum):
    cheapest = "cheapest"
    most_expensive = "most_expensive"
    category = "category"


class GlobalFeeSettings(db.Model, ModelMixin):
    __tablename__ = "global_fee_settings"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    service_fee: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=5)
    bank_fee: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=6)
    tickets_sorting_by: orm.Mapped[str] = orm.mapped_column(
        sa.String(32),
        default=TicketsSortingType.cheapest.value,
        server_default=TicketsSortingType.cheapest.value,
    )

    def __repr__(self):
        return f"<GlobalFeeSettings: service_fee:{self.service_fee}, bank_fee:{self.bank_fee}, sorting:{self.tickets_sorting_by}>"
