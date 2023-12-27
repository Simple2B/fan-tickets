from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class User(BaseModel):
    id: int
    username: str | None = None
    email: str
    unique_id: str
    name: str | None = None
    last_name: str | None = None
    activated: bool
    phone: str | None = None
    address: str | None = None
    facebook: str | None = None
    instagram: str | None = None
    twitter: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)
