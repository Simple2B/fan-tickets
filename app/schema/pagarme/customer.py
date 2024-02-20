from typing import Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from .api import PagarPaging


class PagarCustomerGender(Enum):
    male = "male"
    female = "female"


class PagarmeCustomerMobilePhone(BaseModel):
    country_code: str
    area_code: str
    number: str

    model_config = ConfigDict(from_attributes=True)


class PagarmeCustomerPhones(BaseModel):
    mobile_phone: PagarmeCustomerMobilePhone
    # mobile_phone: str

    model_config = ConfigDict(from_attributes=True)


class PagarmeCustomerCreate(BaseModel):
    name: str
    birthdate: str
    code: str
    email: str
    document: str
    type: str = "individual"
    phones: PagarmeCustomerPhones

    model_config = ConfigDict(from_attributes=True)


class PagarmeCustomerInput(BaseModel):
    id: str
    name: str
    birthdate: str
    email: str
    code: str
    delinquent: bool = False
    phone: dict = {}

    model_config = ConfigDict(from_attributes=True)


class PagarmeCustomerOutput(BaseModel):
    id: str
    name: str
    birthdate: str
    email: str | None = None
    code: str | None = None
    delinquent: bool = False
    phone: dict = {}

    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class PagarmeCustomers(BaseModel):
    data: list[PagarmeCustomerOutput]

    model_config = ConfigDict(from_attributes=True)


class PagarCustomerListQuery(BaseModel):
    name: Optional[str] = None
    document: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[PagarCustomerGender] = None
    page: Optional[int] = None
    size: Optional[int] = None
    code: Optional[int] = None


class PagarCustomerOut(BaseModel):
    id: str
    name: str
    delinquent: bool
    created_at: datetime
    updated_at: datetime
    birthdate: datetime


class PagarCustomerListResponse(BaseModel):
    paging: PagarPaging
    data: list[PagarCustomerOut]
