from pydantic import (
    BaseModel,
)

from app.schema.user import User
from app.schema.room import Room
from pydantic_settings import SettingsConfigDict


class ChatAuthParams(BaseModel):
    room_unique_id: str | None = None
    user_unique_id: str | None = None
    email: str | None = None
    password: str | None = None
    confirm_password: str | None = None
    verification_code: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthResultParams(BaseModel):
    user: User
    room: Room
    now_str: str
    params: ChatAuthParams

    model_config = SettingsConfigDict(from_attributes=True)
