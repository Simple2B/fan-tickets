import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db
from .utils import ModelMixin


class Translation(db.Model, ModelMixin):
    __tablename__ = "translations"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    en: orm.Mapped[str] = orm.mapped_column(sa.Text)
    pt: orm.Mapped[str] = orm.mapped_column(sa.Text)

    def __repr__(self) -> str:
        return f"<en {self.en} - pt {self.pt}>"
