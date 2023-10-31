from typing import Any
import sqlalchemy as sa
from app import db
from uuid import uuid4


class ModelMixin(object):
    def save(self, commit=True):
        # Save this model to the database.
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        # Save this model to the database.
        db.session.delete(self)
        if commit:
            db.session.commit()
        return self

    @classmethod
    def count(cls) -> int:
        # Return count records of model.
        return db.session.scalar(sa.select(sa.func.count()).select_from(cls))

    @classmethod
    def all(cls) -> list[Any]:
        # Return all records of model.
        return db.session.scalars(sa.select(cls)).all()

    @classmethod
    def first(cls) -> Any | None:
        # Return first record of model.
        return db.session.scalar(sa.select(cls))

    @classmethod
    def get(cls, id: int) -> Any | None:
        # Return record of model by id.
        return db.session.get(cls, id)


def count(stmt: sa.sql.selectable.Select) -> int:
    # Return count of query.
    return db.session.scalar(sa.select(sa.func.count()).select_from(stmt.subquery()))


def all(stmt: sa.sql.selectable.Select) -> list[Any]:
    # Return all records of query.
    return db.session.scalars(stmt).all()


def first(stmt: sa.sql.selectable.Select) -> Any | None:
    # Return first record of query.
    return db.session.scalar(stmt)


def paginate(
    stmt: sa.sql.selectable.Select, page: int, per_page: int
) -> list[Any] | None:
    # Return records of query by page and per_page.
    return db.session.scalars(stmt.offset((page - 1) * per_page).limit(per_page)).all()


def gen_uuid() -> str:
    return str(uuid4())
