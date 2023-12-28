from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class PagarmeError(BaseModel):
    status_code: int
    error: str
    details: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class UserMobilePhone(BaseModel):
    country_code: str
    area_code: str
    number: str

    model_config = SettingsConfigDict(from_attributes=True)


class UserPhones(BaseModel):
    mobile_phone: UserMobilePhone

    model_config = SettingsConfigDict(from_attributes=True)


class PagarmeUserCreate(BaseModel):
    name: str
    birthdate: str
    code: str
    email: str
    document: str
    type: str = "individual"
    phones: UserPhones

    model_config = SettingsConfigDict(from_attributes=True)


class PagarmeUpdateUserOutput(BaseModel):
    """
        {
      "id": "cus_o873mYLFOFlVRe0D",
      "name": "UpdatedTestingCustomer",
      "delinquent": false,
      "created_at": "2023-12-28T12:16:35Z",
      "updated_at": "2023-12-28T12:17:06Z",
      "birthdate": "2000-02-02T00:00:00Z",
      "phones": {}
    }
    """

    id: str
    name: str
    delinquent: bool
    created_at: str
    updated_at: str
    birthdate: str
    phones: dict


class PagarmeUserInput(BaseModel):
    id: str
    name: str
    birthdate: str
    email: str
    code: str
    delinquent: bool = False
    phones: dict = {}

    model_config = SettingsConfigDict(from_attributes=True)


class PagarmeUserOutput(PagarmeUserInput):
    created_at: str
    updated_at: str

    model_config = SettingsConfigDict(from_attributes=True)


class PagarmeUsers(BaseModel):
    data: list[PagarmeUserOutput]

    model_config = SettingsConfigDict(from_attributes=True)


class PagarmeBillingAddress(BaseModel):
    line_1: str
    line_2: str | None = None
    zip_code: str
    city: str
    state: str
    country: str


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
    customer: PagarmeUserOutput
    billing_address: PagarmeBillingAddress

    model_config = SettingsConfigDict(from_attributes=True)


class PagarmeCardInput(PagarmeCard):
    card_id: str

    model_config = SettingsConfigDict(from_attributes=True)


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
    number: int
    exp_month: int
    exp_year: int
    cvv: int
    billing_address: PagarmeBillingAddress


class PagarmeCardOutput(PagarmeCard):
    id: str
    created_at: str | None
    updated_at: str | None

    model_config = SettingsConfigDict(from_attributes=True)


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
    category: str

    model_config = SettingsConfigDict(from_attributes=True)


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

    model_config = SettingsConfigDict(from_attributes=True)


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
    customer: PagarmeUserInput | None = None
    customer_id: str | None = None
    code: str | None = None
    payments: list[PagarmeCheckout]

    model_config = SettingsConfigDict(from_attributes=True)


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
    customer: PagarmeUserOutput
    status: str
    created_at: str
    updated_at: str
    closed_at: str | None = None
    charges: list
    checkouts: list

    model_config = SettingsConfigDict(from_attributes=True)


class PagarmeCreditCardPayment(BaseModel):
    status: str
    user_pagar_id: str
    ticket_unique_id: str
    price_paid: float
