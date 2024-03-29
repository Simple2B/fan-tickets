from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class ChatBuyRequiredParams(BaseModel):
    room_unique_id: str

    model_config = SettingsConfigDict(from_attributes=True)


class ChatBuyEventParams(ChatBuyRequiredParams):
    user_message: str | None = None
    renew_search: bool = False
    location_unique_id: str | None = None
    event_name: str | None = None
    tickets_show_all: bool = False
    add_ticket: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatBuyTicketParams(ChatBuyRequiredParams):
    event_unique_id: str | None = None
    ticket_unique_id: str | None = None
    user_message: str | None = None
    ask_payment: bool = False
    has_email: bool = False
    tickets_show_all: bool = False
    add_ticket: bool = False
    from_date_template: bool = False
    from_web: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatBuyTicketWithoutRequiredParams(BaseModel):
    room_unique_id: str | None = None
    event_unique_id: str | None = None
    ticket_unique_id: str | None = None
    user_message: str | None = None
    ask_payment: bool = False
    has_email: bool = False
    tickets_show_all: bool = False
    add_ticket: bool = False
    from_date_template: bool = False
    from_web: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatBuyTicketTotalPrice(BaseModel):
    total: int
    service: int
    net: int
    unique_ids: str

    model_config = SettingsConfigDict(from_attributes=True)


class BookTicketError(BaseModel):
    not_found: bool | None = False
    limit_reached: bool | None = False
    error_message: str | None = None
