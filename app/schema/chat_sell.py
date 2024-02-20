from pydantic import (
    BaseModel,
)

from pydantic_settings import SettingsConfigDict


class ChatSellRequiredParams(BaseModel):
    room_unique_id: str

    model_config = SettingsConfigDict(from_attributes=True)


class ChatSellEventParams(ChatSellRequiredParams):
    user_message: str | None = None
    event_name: str | None = None
    event_category_id: str | None = None
    event_unique_id: str | None = None
    create_event: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class ChatSellTicketParams(ChatSellRequiredParams):
    event_unique_id: str | None = None
    ticket_unique_id: str | None = None
    user_message: str | None = None
    tickets_quantity_answer: str | None = None
    ticket_type: str | None = None
    ticket_category: str | None = None
    ticket_has_section: bool = True
    ticket_section: str | None = None
    ticket_has_queue: bool = True
    ticket_queue: str | None = None
    ticket_has_seat: bool = True
    ticket_seat: str | None = None
    ticket_notes: str | None = None
    ticket_price: int | None = None
    ticket_paired: bool = False

    model_config = SettingsConfigDict(from_attributes=True)


class BardRequestDataContentPart(BaseModel):
    text: str


class BardRequestDataContent(BaseModel):
    role: str = "user"
    parts: list[BardRequestDataContentPart]


class BardRequestData(BaseModel):
    """
    data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": message},
                    ],
                }
            ]
        }
    """

    contents: list[BardRequestDataContent]
