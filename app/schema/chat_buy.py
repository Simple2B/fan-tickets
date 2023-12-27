from pydantic import (
    BaseModel,
)

from pydantic_settings import SettingsConfigDict


class ChatRequiredParams(BaseModel):
    room_unique_id: str

    model_config = SettingsConfigDict(from_attributes=True)
