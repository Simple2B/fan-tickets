from pydantic import BaseModel


class GenericError(BaseModel):
    error: str
    details: str
