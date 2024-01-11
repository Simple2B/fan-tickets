from typing import Optional
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .customer import PagarmeCustomerOutput, PagarmeCustomerInput, PagarmeCustomerCreate, PagarCustomerOut
from .api import PagarmeGatewayResponse, PagarmeAntifraudResponse


class PagarmeBillingAddress(BaseModel):
    country: str
    state: str
    line_1: str
    line_2: str | None = None
    zip_code: str
    city: str


class PagarmePhoneData(BaseModel):
    country_code: Optional[str] = None
    area_code: Optional[str] = None
    number: Optional[str] = None


class PagarmePhonesData(BaseModel):
    home_phone: Optional[PagarmePhoneData] = None
    mobile_phone: Optional[PagarmePhoneData] = None


class PagarmeShippingData(BaseModel):
    amount: Optional[int] = None
    description: Optional[str] = None
    recipient_name: Optional[str] = None
    recipient_phone: Optional[str] = None
    address: Optional[PagarmeBillingAddress] = None


class PagarmeCard(BaseModel):
    """
    '{"id": "card_lD6BoyphvHaLVv0y",
    "first_six_digits": "424242",
    "last_four_digits": "4242",
    "brand": "Visa",
    "holder_name": "bob",
    "exp_month": 1,
    "exp_year": 2025,
    "status": "active",
    "type": "credit",
    "created_at": "2023-12-21T12:24:03Z",
    "updated_at": "2023-12-21T12:24:03Z",
    "customer": {
        "id": "cus_rQ9znDrHaeilEa8q",
        "name": "bob",
        "delinquent": false,
        "created_at": "2023-12-21T12:24:02Z",
        "updated_at": "2023-12-21T12:24:02Z",
        "birthdate": "2000-01-01T00:00:00Z",
        "phones": {}\r\n  }
        }'
    """

    first_six_digits: str
    last_four_digits: str
    brand: str
    holder_name: str
    exp_month: int
    exp_year: int
    status: str
    type: str
    customer: Optional[PagarmeCustomerOutput] = None
    billing_address: PagarmeBillingAddress

    model_config = ConfigDict(from_attributes=True)


class PagarmeCardInput(PagarmeCard):
    card_id: str

    model_config = ConfigDict(from_attributes=True)


class PagarmeCardCreate(BaseModel):
    """
    payload = {
        "customer_id": customer_id,
        "holder_name": holder_name,
        "number": number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvv": cvv,
        "billing_address": billing_address,
    }
    """

    customer_id: str
    holder_name: str
    number: str
    exp_month: int
    exp_year: int
    cvv: int
    billing_address: PagarmeBillingAddress


class PagarmeCardOutput(PagarmeCard):
    id: str
    created_at: str | None
    updated_at: str | None

    model_config = ConfigDict(from_attributes=True)


class PagarmeItem(BaseModel):
    """
    amount: integer
    description: string
    quantity: integer
    category: string
    """

    amount: int
    code: str
    description: str
    quantity: int
    category: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PagarmeCheckout(BaseModel):
    """
    expires_in: integer
    billing_address_editable: boolean
    customer_editable: boolean
    accepted_payment_methods: array of strings
    success_url: string
    """

    expires_in: int
    payment_method: str
    billing_address_editable: bool
    customer_editable: bool
    accepted_payment_methods: list[str]
    success_url: str
    credit_card: PagarmeCardInput

    model_config = ConfigDict(from_attributes=True)


class PagarmeAdditionalInformation(BaseModel):
    name: str
    value: str

    model_config = ConfigDict(from_attributes=True)


class PagarmePix(BaseModel):
    expires_in: int
    additional_information: list[PagarmeAdditionalInformation]

    model_config = ConfigDict(from_attributes=True)


class PagarmePixPayment(BaseModel):
    payment_method: str
    pix: list[PagarmePix]


class PagarmeCreateOrderInput(BaseModel):
    """
    {
        "items":[...],
        "customer":{...},
        "payments":[
            {
                "amount" : 3000,
                "payment_method":"checkout",
                "checkout": {
                    "expires_in":120,
                    "billing_address_editable" : false,
                    "customer_editable" : true,
                    "accepted_payment_methods": ["credit_card"],
                    "success_url": "https://www.pagar.me",
                    "credit_card": {...}
                }
            }
        ]
    }
    """

    items: list[PagarmeItem]
    customer: PagarmeCustomerInput | None = None
    customer_id: str | None = None
    code: str | None = None
    payments: list[PagarmeCheckout]

    model_config = ConfigDict(from_attributes=True)


class PagarmeCreateOrderOutput(BaseModel):
    """
    customer: object
    customer_id: string
    items: array of objects
    payments: array of objects [credit_card, checkout, pix]
    """

    id: str
    code: str
    amount: int
    currency: str
    closed: bool
    items: list[PagarmeItem]
    customer: PagarmeCustomerOutput
    status: str
    created_at: str
    updated_at: str
    closed_at: str | None = None
    charges: list
    checkouts: list

    model_config = ConfigDict(from_attributes=True)


class PagarmeCreditCardPayment(BaseModel):
    status: str
    user_pagar_id: str
    ticket_unique_id: str
    price_paid: float


class PagarmeOrderItemCreate(BaseModel):
    amount: Optional[int] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    code: str


class PagarmeDocumentType(Enum):
    CPF = "CPF"
    CNPJ = "CNPJ"


class PagarmeCheckoutData(BaseModel):
    expires_in: Optional[int] = None
    default_payment_method: Optional[str] = None
    accepted_payment_methods: Optional[list[str]] = None
    accepted_brands: Optional[str] = None
    accepted_multi_payment_methods: Optional[str] = None
    success_url: Optional[str] = None
    skip_checkout_success_page: Optional[bool] = None
    customer_editable: Optional[bool] = None
    billing_address_editable: Optional[bool] = None
    billing_address: Optional[PagarmeBillingAddress] = None


class PagarmePaymentData(BaseModel):
    amount: Optional[str] = None
    checkout: PagarmeCheckoutData


class PagarmeOrderCreateData(BaseModel):
    code: Optional[str] = None
    items: list[PagarmeOrderItemCreate]
    customer_id: Optional[str] = None
    customer: Optional[PagarmeCustomerCreate] = None
    shipping: Optional[PagarmeShippingData] = None
    payments: list[PagarmePaymentData]
    metadata: Optional[dict] = None


class PagarmeCheckoutDetailsData(BaseModel):
    expires_in: int
    default_payment_method: str = "checkout"
    accepted_payment_methods: list[str]


class PagarmeCheckoutSplitOptions(BaseModel):
    charge_processing_fee: bool
    charge_remainder_fee: bool
    liable: bool


class PagarmeCheckoutSplitData(BaseModel):
    amount: int
    recipient_id: str
    type: str
    options: list[PagarmeCheckoutSplitOptions]


class PagarmePaymentCheckoutData(BaseModel):
    payment_method: str = "checkout"
    checkout: PagarmeCheckoutDetailsData
    amount: int
    split: list[PagarmeCheckoutSplitData]


class PagarmeOrderCheckoutCreateData(PagarmeOrderCreateData):
    payments: list[PagarmePaymentData]


class PagarmeOrderCreditCardCreate(BaseModel):
    code: Optional[str] = None
    items: list[PagarmeOrderItemCreate]
    customer_id: Optional[str] = None
    customer: Optional[PagarmeCustomerCreate] = None
    shipping: Optional[PagarmeShippingData] = None
    payments: list[PagarmePaymentData]
    metadata: Optional[dict] = None


class PagarmeTransactionOut(BaseModel):
    id: str
    transaction_type: str
    gateway_id: str
    amount: int
    status: str
    success: bool
    installments: int
    acquirer_name: str
    acquirer_tid: str
    acquirer_nsu: str
    acquirer_auth_code: str
    acquirer_message: str
    acquirer_return_code: str
    operation_type: str
    card: PagarmeCard
    funding_source: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    gateway_response: PagarmeGatewayResponse
    antifraud_response: PagarmeAntifraudResponse
    metadata: dict


class PagarmeCharge(BaseModel):
    id: str
    code: str
    gateway_id: str
    amount: int
    paid_amount: int
    status: str
    currency: str
    payment_method: str
    created_at: datetime
    paid_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    customer: PagarCustomerOut
    last_transaction: Optional[PagarmeTransactionOut] = None


class PagarmeOrderOut(BaseModel):
    id: str
    code: str
    amount: int
    currency: str
    closed: bool
    items: list[PagarmeItem]
    customer: PagarCustomerOut
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    charges: list[PagarmeCharge]
