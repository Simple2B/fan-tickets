from datetime import datetime
from pydantic import BaseModel


class Event(BaseModel):
    name: str
    image: bytes | None = None
    url: str
    observations: str
    warning: str
    date_time: datetime
    location_id: int
    category_id: int
    creator_id: int

    # model_config: ConfigDict = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }


class Events(BaseModel):
    events: list[Event]

    class Config:
        orm_mode = True