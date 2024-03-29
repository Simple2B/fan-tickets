from pydantic import BaseModel
from .payment import PagarmeItem, PagarmePaymentPix, PagarmePaymentSplit


class PagarmeCreateOrder(BaseModel):
    items: list[PagarmeItem]
    customer_id: str
    code: str | None = None


class PagarmeCreateOrderPix(PagarmeCreateOrder):
    expires_at: str = "2030-12-31T23:59:59Z"
    payments: list[PagarmePaymentPix]


class PagarmeCreateOrderSplit(PagarmeCreateOrder):
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
