from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class Room(BaseModel):
    id: int
    unique_id: str
    type_of: str
    is_open: bool
    ticket_id: int | None = None
    seller_id: int | None = None
    buyer_id: int | None = None

    model_config = SettingsConfigDict(from_attributes=True)
