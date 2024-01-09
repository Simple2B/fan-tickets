from typing import Optional
from pydantic import ConfigDict, BaseModel


class PagarmeError(BaseModel):
    status_code: int
    error: str
    details: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PagarPaging(BaseModel):
    total: int
    previous: str = ""
    next: str = ""


class PagarmePaginationQuery(BaseModel):
    page: Optional[str] = None
    size: Optional[str] = None


class PagarmeGatewayResponse(BaseModel):
    code: int


class PagarmeAntifraudResponse(BaseModel):
    status: str
    score: str
    provider_name: str
