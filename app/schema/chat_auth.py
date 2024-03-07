from pydantic import (
    BaseModel,
)

from pydantic_settings import SettingsConfigDict


class ChatRequiredParams(BaseModel):
    room_unique_id: str

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthEmailParams(ChatRequiredParams):
    ticket_unique_id: str | None = None
    user_message: str | None = None
    from_sign_up: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthRequiredParams(ChatRequiredParams):
    user_unique_id: str

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthParams(ChatAuthRequiredParams):
    ticket_unique_id: str | None = None
    user_message: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthSocialProfileParams(ChatAuthRequiredParams):
    user_message: str | None = None
    without_social_profile: bool = False
    without_facebook: bool = False
    facebook: bool = False
    without_twitter: bool = False
    twitter: bool = False
    without_instagram: bool = False
    instagram: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthResultParams(BaseModel):
    error_message: str | None = None
    is_error: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthEmailValidate(BaseModel):
    email: str
    verification_code: int | None = None
    message: str | None = None
    is_error: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatAuthPhoneValidate(BaseModel):
    phone: str
    message: str | None = None
    is_error: bool = False

    model_config = SettingsConfigDict(from_attributes=True)
