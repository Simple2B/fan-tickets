import base64
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
    filename: orm.Mapped[str] = orm.mapped_column(sa.String(256))
    mimetype: orm.Mapped[str] = orm.mapped_column(sa.String(32), default="image/png")
    file: orm.Mapped[bytes] = orm.mapped_column(sa.LargeBinary)

    @property
    def base64_src(self) -> str:
        """
        Returns the base64 representation of the picture.
        """
        base64_img = base64.b64encode(self.file).decode("utf-8")
        return f"data:image/png;base64,{ base64_img }"

    def __repr__(self):
        return f"<{self.id}: {self.filename}.{self.mimetype}>"
