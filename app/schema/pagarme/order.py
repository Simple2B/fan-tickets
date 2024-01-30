from pydantic import BaseModel
from .payment import PagarmeItem, PagarmePaymentPix


class PagarmeCreateOrderPix(BaseModel):
    items: list[PagarmeItem]
    customer_id: str
    code: str | None = None
    payments: list[PagarmePaymentPix]


class PagarmeChargeTransactionPix(BaseModel):
    qr_code_url: str


class PagarmeOrderChargeOutPix(BaseModel):
    last_transaction: PagarmeChargeTransactionPix


class PagarmeCreateOrderResponsePix(BaseModel):
    status: str
    code: str
    id: str
    charges: list[PagarmeOrderChargeOutPix]
