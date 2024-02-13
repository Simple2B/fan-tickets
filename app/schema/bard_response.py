from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class QuestionToBard(BaseModel):
    text: str

    model_config = SettingsConfigDict(from_attributes=True)


class BardRequestContents(BaseModel):
    role: str = "user"
    parts: list[QuestionToBard]

    model_config = SettingsConfigDict(from_attributes=True)


class BardRequest(BaseModel):
    """
    data = {"contents": [{"role": "user", "parts": [{"text": "What is the difference between python and javascript?"}]}]}
    """

    contents: list[BardRequestContents]

    model_config = SettingsConfigDict(from_attributes=True)


class BardResponse(BaseModel):
    """
    bard_response.json()["candidates"][0]["content"]["parts"][0]["text"]
    """

    event_name: str | None = None
    official_url: str | None = None
    location: str | None = None
    venue: str | None = None
    date: str | None = None
    time: str | None = None
    date_time: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)
