from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class BardResponse(BaseModel):
    event_name: str
    official_url: str
    location: str
    venue: str
    date: str
    time: str

    model_config = SettingsConfigDict(from_attributes=True)
