from pydantic import BaseModel
from .payment import PagarmeItem, PagarmePaymentPix, PagarmeCharge


class PagarmeCreateOrderPix(BaseModel):
    items: list[PagarmeItem]
    customer_id: str
    code: str
    payments: list[PagarmePaymentPix]


class PagarmeChargeTransactionPix(BaseModel):
    qr_code_url: str


class PagarmeOrderChargeOutPix(BaseModel):
    last_transaction: PagarmeChargeTransactionPix


class PagarmeCreateOrderResponsePix(BaseModel):
    status: str
    charges: list[PagarmeOrderChargeOutPix]
