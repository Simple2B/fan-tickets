from app import db
from uuid import uuid4


class ModelMixin(object):
    def save(self, commit=True):
        # Save this model to the database.
        db.session.add(self)
        if commit:
            db.session.commit()
        return self


def gen_uuid() -> str:
    return str(uuid4())
