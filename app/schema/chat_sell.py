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

    model_config = SettingsConfigDict(from_attributes=True)


class ChatSellResultParams(BaseModel):
    now_str: str
    is_error: bool = False

    model_config = SettingsConfigDict(from_attributes=True)
