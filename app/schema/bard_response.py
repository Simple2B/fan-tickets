from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from .event import Event


class BardResponse(BaseModel):
    event_name: str | None = None
    official_url: str | None = None
    location: str | None = None
    date: str | None = None
    time: str | None = None
    date_time: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class EventValidation(BaseModel):
    events: list[Event] | None = None
    bard_response: BardResponse | None = None

    model_config = SettingsConfigDict(from_attributes=True)
