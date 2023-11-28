from typing_extensions import Annotated
from datetime import datetime
from pydantic import (
    BaseModel,
    ValidationError,
    ValidatorFunctionWrapHandler,
    ValidationInfo,
)
from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import WrapValidator

from pydantic_settings import SettingsConfigDict


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def parse_datetime_from_str(
    v: str | datetime, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> datetime:
    if info.mode == "json":
        assert isinstance(v, str), "In JSON mode the input must be a string!"
        # you can call the handler multiple times
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())
    assert info.mode == "python"
    if isinstance(v, datetime):
        return v
    assert isinstance(v, str), "In Python mode the input must be an str!"
    # do no further validation
    return datetime.strptime(v, DATETIME_FORMAT)


DateTime = Annotated[
    datetime,
    PlainSerializer(
        # lambda dt: dt.strftime(DATETIME_FORMAT),
        lambda dt: dt.isoformat(),
        return_type=str,
        when_used="always",
    ),
    WrapValidator(parse_datetime_from_str),
]


class Event(BaseModel):
    unique_id: str
    name: str
    image: bytes | None = None
    url: str
    observations: str
    warning: str
    date_time: DateTime
    location_id: int
    category_id: int
    creator_id: int

    model_config = SettingsConfigDict(from_attributes=True)


class Events(BaseModel):
    user_id: int
    events: list[Event]

    model_config = SettingsConfigDict(from_attributes=True)


class EventsInput(BaseModel):
    location: str | None = None
    date_from: str | None = None
    date_to: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class EventFilter(BaseModel):
    location: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    event_per_page: int = 0  # additional events on the page
    categories: list[str]

    model_config = SettingsConfigDict(from_attributes=True)
