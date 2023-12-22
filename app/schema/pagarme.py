from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict


class PagarmeUserInput(BaseModel):
    id: str
    name: str
    birthdate: str
    email: str
    code: str
    delinquent: bool = False
    phone: dict = {}

    model_config = SettingsConfigDict(from_attributes=True)


class PagarmeUserOutput(PagarmeUserInput):
    created_at: str
    updated_at: str

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
    payments: array of objects [credit_card: object, boleto: object, pix: object]
    """

    customer: PagarmeUserOutput
    customer_id: str
    items: list[PagarmeItem]
    payments: list[PagarmeCheckout]

    model_config = SettingsConfigDict(from_attributes=True)
