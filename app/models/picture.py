import sqlalchemy as sa
from sqlalchemy import orm
from .utils import ModelMixin
from app.database import db


class Picture(db.Model, ModelMixin):
    """
    The model for any picture that is uploaded to the server.
    Users, events, locations and categories have have fk on a picture.
    """

    __tablename__ = "pictures"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    filename: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)
    mimetype: orm.Mapped[str] = orm.mapped_column(sa.String(32), default="image/png")
    file: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary, nullable=False)

    def __repr__(self):
        return f"<{self.id}: {self.filename}.{self.mimetype}>"
