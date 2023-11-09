from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class User(BaseModel):
    id: int
    username: str
    email: str
    activated: bool

    model_config = SettingsConfigDict(from_attributes=True)
