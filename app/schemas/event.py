from datetime import datetime
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class Event(BaseModel):
    unique_id: str
    name: str
    image: bytes | None = None
    url: str
    observations: str
    warning: str
    date_time: datetime
    location_id: int
    category_id: int
    creator_id: int

    model_config = SettingsConfigDict(from_attributes=True)


class Events(BaseModel):
    user_id: int
    events: list[Event]

    model_config = SettingsConfigDict(from_attributes=True)
