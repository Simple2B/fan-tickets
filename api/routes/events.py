from fastapi import Depends, APIRouter, status

import app.models as m
from app.logger import log

from api.dependency import get_current_user


events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.get("/by_id", status_code=status.HTTP_200_OK)
def get_event_by_id(
    current_user: m.User = Depends(get_current_user),
):
    """Returns the current user profile"""

    log(log.INFO, f"User {current_user.username} requested his profile")
    return current_user
