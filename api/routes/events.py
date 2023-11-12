from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as m
from app.logger import log

from api.dependency import get_current_user


events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.get("/by_id", status_code=status.HTTP_200_OK)
def get_event_by_id(
    event_unique_id: str,
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns an event by its unique id"""

    events = db.scalars(m.Event.select()).all()
    log(log.INFO, f"User {current_user.username} requested his profile")
    return current_user
