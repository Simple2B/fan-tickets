from pydantic import (
    BaseModel,
)

from pydantic_settings import SettingsConfigDict


class ChatBuyRequiredParams(BaseModel):
    room_unique_id: str

    model_config = SettingsConfigDict(from_attributes=True)


class ChatBuyEventParams(ChatBuyRequiredParams):
    user_message: str | None = None
    renew_search: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatBuyTicketParams(ChatBuyRequiredParams):
    event_unique_id: str | None = None
    ticket_unique_id: str | None = None
    user_message: str | None = None
    ticket_type: str | None = None
    ticket_category: str | None = None
    ticket_has_section: bool = True
    ticket_section: str | None = None
    ticket_has_queue: bool = True
    ticket_queue: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)
