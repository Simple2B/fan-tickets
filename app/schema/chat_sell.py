from pydantic import (
    BaseModel,
)

from pydantic_settings import SettingsConfigDict


class ChatSellParams(BaseModel):
    room_unique_id: str
    event_name: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)
