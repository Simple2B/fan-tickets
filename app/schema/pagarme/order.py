from pydantic import BaseModel
from .payment import PagarmeItem, PagarmePaymentPix, PagarmePaymentSplit


class PagarmeCreateOrderPix(BaseModel):
    items: list[PagarmeItem]
    customer_id: str
    code: str | None = None
    payments: list[PagarmePaymentPix]


class PagarmeCreateOrderSplit(PagarmeCreateOrderPix):
    payments: list[PagarmePaymentSplit]


class PagarmeChargeTransactionPix(BaseModel):
    qr_code: str
    qr_code_url: str
    success: bool


class PagarmeOrderChargeOutPix(BaseModel):
    last_transaction: PagarmeChargeTransactionPix


class PagarmeCreateOrderResponsePix(BaseModel):
    status: str
    code: str
    id: str
    charges: list[PagarmeOrderChargeOutPix]
