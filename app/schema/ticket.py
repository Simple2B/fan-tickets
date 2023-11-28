from pydantic import (
    BaseModel,
)

from pydantic_settings import SettingsConfigDict

from config import config

CFG = config()


class TicketFilter(BaseModel):
    location: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    ticket_per_page: int = 0  # additional tickets on the page
    q: str | None = None
    categories: list[str]
    event_id: int | None = None

    model_config = SettingsConfigDict(from_attributes=True)
