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


class DefaultBankAccount(BaseModel):
    holder_name: str
    holder_type: str = "individual"
    holder_document: str
    bank: str
    branch_number: str
    branch_check_digit: str
    account_number: str
    account_check_digit: str
    type: str = "checking"


class PagarmeRecipientCreate(BaseModel):
    name: str
    email: str
    description: str
    document: str
    type: str = "individual"
    code: str
    default_bank_account: DefaultBankAccount
