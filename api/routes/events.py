from datetime import datetime
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as m
from app import schema as s
from app.logger import log

from api.dependency import get_current_user


events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.post("/", status_code=status.HTTP_200_OK, response_model=s.Events)
def get_events(
    events_input: s.EventsInput,
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns events by location, date_from or date_to"""

    events_query = m.Event.select()
    if events_input.location:
        events_query = events_query.where(
            m.Event.location.has(name=events_input.location)
        )
        log(log.INFO, "events queried by location [%s]: ", events_input.location)
    if events_input.date_from:
        date_from = datetime.fromisoformat(events_input.date_from)
        events_query = events_query.where(m.Event.date_time >= date_from)
        log(log.INFO, "events queried by date_from [%s]: ", events_input.date_from)
    if events_input.date_to:
        date_to = datetime.fromisoformat(events_input.date_to)
        events_query = events_query.where(m.Event.date_time <= date_to)
        log(log.INFO, "events queried by date_to [%s]: ", events_input.date_to)
    events = db.scalars(events_query).all()
    log(log.INFO, f"Events queried: {events}")
    return s.Events(
        user_id=current_user.id,
        events=events,
    ).model_dump()


@events_router.get("/by_id", status_code=status.HTTP_200_OK, response_model=s.Event)
def get_event_by_id(
    event_unique_id: str,
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns an event by its unique id"""

    if not event_unique_id:
        log(log.ERROR, "event_unique_id is empty")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="event_unique_id is empty",
        )
    event = db.scalar(m.Event.select().where(m.Event.unique_id == event_unique_id))
    log(log.INFO, f"Event got: {event}")
    try:
        event = s.Event.model_validate(event)
    except Exception as e:
        log(log.ERROR, f"Event validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Event validation failed: {e}",
        )
    return event.model_dump()
