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
    service_fee_buyer: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=2, server_default="2")
    service_fee_seller: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=3, server_default="3")
    bank_fee_buyer: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=4, server_default="4")
    bank_fee_seller: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=2, server_default="2")
    tickets_sorting_by: orm.Mapped[str] = orm.mapped_column(
        sa.String(32),
        default=TicketsSortingType.cheapest.value,
        server_default=TicketsSortingType.cheapest.value,
    )
    selling_limit: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=5, server_default="5")
    buying_limit: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=3, server_default="3")
    limit_per_event: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=5, server_default="2")

    @property
    def service_fee(self):
        return self.service_fee_buyer + self.service_fee_seller

    @property
    def bank_fee(self):
        return self.bank_fee_buyer + self.bank_fee_seller

    def __repr__(self):
        return f"<GlobalFeeSettings: service_fee:{self.service_fee}, bank_fee:{self.bank_fee}, sorting:{self.tickets_sorting_by}>"
