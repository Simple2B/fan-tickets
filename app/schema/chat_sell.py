from pydantic import (
    BaseModel,
)

from pydantic_settings import SettingsConfigDict


class ChatSellParams(BaseModel):
    room_unique_id: str

    event_name: str | None = None
    event_location: str | None = None
    event_date: str | None = None
    event_time: str | None = None
    event_category: str | None = None
    event_unique_id: str | None = None

    ticket_type: str | None = None
    ticket_unique_id: str | None = None
    ticket_category: str | None = None
    ticket_has_section: bool = True
    ticket_section: str | None = None
    ticket_has_queue: bool = True
    ticket_queue: str | None = None
    ticket_has_seat: bool = True
    ticket_seat: str | None = None
    ticket_has_notes: bool = True
    ticket_notes: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class ChatSellResultParams(BaseModel):
    now_str: str
    is_error: bool = False

    model_config = SettingsConfigDict(from_attributes=True)
