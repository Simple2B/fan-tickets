from pydantic import (
    BaseModel,
)

from pydantic_settings import SettingsConfigDict


class ChatAuthParams(BaseModel):
    room_unique_id: str
    user_unique_id: str | None = None
    email: str | None = None
    verification_code: str | None = None
    name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None
    birth_date: str | None = None
    without_social_profile: bool = False
    facebook: str | None = None
    instagram: str | None = None
    twitter: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthResultParams(BaseModel):
    now_str: str
    params: ChatAuthParams
    is_error: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthEmailValidate(BaseModel):
    email: str
    message: str | None = None
    is_error: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthPhoneValidate(BaseModel):
    phone: str
    message: str | None = None
    is_error: bool = False

    model_config = SettingsConfigDict(from_attributes=True)
