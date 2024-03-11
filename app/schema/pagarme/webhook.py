from pydantic import BaseModel, ConfigDict


class PagarmeWebhookCustomer(BaseModel):
    """
    "id": "cus_PMkWepVUrSbG3gr1",
    "name": "Alexandre",
    "email": "amonteiro.sp@gmail.com",
    "code": "09308007-332c-41f2-9642-1e3e0e7ac33b",
    "document": "13100180810",
    "type": "individual",
    "delinquent": False,
    "created_at": "2024-02-22T18:20:04.927Z",
    "updated_at": "2024-02-22T18:20:04.927Z",
    "birthdate": "1969-11-19T00:00:00Z",
    "phones": {"mobile_phone": {"country_code": "55", "number": "98555880", "area_code": "11"}},
    "metadata": {},
    """

    id: str
    name: str
    email: str
    code: str
    document: str
    type: str
    delinquent: bool
    created_at: str
    updated_at: str
    birthdate: str
    phones: dict
    metadata: dict | None = {}


class PagarmeWebhookItem(BaseModel):
    """
    {
        "id": "oi_g24ypnnSqwU2aPWm",
        "amount": 100,
        "category": "Concert Event",
        "created_at": "2024-02-23T13:02:02.0466667Z",
        "description": "9e4f87a2-3102-4b02-8d77-bf6fabcbbabc, ",
        "quantity": 1,
        "status": "active",
        "updated_at": "2024-02-23T13:02:02.0466667Z",
    }
    """

    id: str
    amount: int
    category: str
    created_at: str
    description: str
    quantity: int
    status: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class PagarmePaidWebhookData(BaseModel):
    id: str
    code: str
    amount: int
    currency: str
    closed: bool
    items: list[PagarmeWebhookItem]
    customer: PagarmeWebhookCustomer
    status: str
    created_at: str
    updated_at: str
    closed_at: str
    charges: list
    metadata: dict | None = {}

    model_config = ConfigDict(from_attributes=True)


class PagarmePaidWebhook(BaseModel):
    """
        {
        "id": "hook_Xd5nq8XFLGiajz7B",
        "account": {"id": "acc_o21x3QNsVIpVY8Rq", "name": "FANTICKET"},
        "type": "order.paid",
        "created_at": "2024-02-23T13:03:17.4877818Z",
        "data": {
            "id": "or_21E0LVKFVXcpe3rX",
            "code": "57DHDNBK18",
            "amount": 100,
            "currency": "BRL",
            "closed": True,
            "items": [
                {
                    "id": "oi_g24ypnnSqwU2aPWm",
                    "amount": 100,
                    "category": "Concert Event",
                    "created_at": "2024-02-23T13:02:02.0466667Z",
                    "description": "9e4f87a2-3102-4b02-8d77-bf6fabcbbabc, ",
                    "quantity": 1,
                    "status": "active",
                    "updated_at": "2024-02-23T13:02:02.0466667Z",
                }
            ],
            "customer": {
                "id": "cus_PMkWepVUrSbG3gr1",
                "name": "Alexandre",
                "email": "amonteiro.sp@gmail.com",
                "code": "09308007-332c-41f2-9642-1e3e0e7ac33b",
                "document": "13100180810",
                "type": "individual",
                "delinquent": False,
                "created_at": "2024-02-22T18:20:04.927Z",
                "updated_at": "2024-02-22T18:20:04.927Z",
                "birthdate": "1969-11-19T00:00:00Z",
                "phones": {"mobile_phone": {"country_code": "55", "number": "98555880", "area_code": "11"}},
                "metadata": {},
            },
            "status": "paid",
            "created_at": "2024-02-23T13:02:02.047Z",
            "updated_at": "2024-02-23T13:02:38.657509Z",
            "closed_at": "2024-02-23T13:02:02.047Z",
            "charges": [
                {
                    "id": "ch_5EnXkOcvjHOPXLj0",
                    "code": "57DHDNBK18",
                    "gateway_id": "2379366004",
                    "amount": 100,
                    "paid_amount": 100,
                    "status": "paid",
                    "currency": "BRL",
                    "payment_method": "pix",
                    "paid_at": "2024-02-23T13:02:35Z",
                    "created_at": "2024-02-23T13:02:02.077Z",
                    "updated_at": "2024-02-23T13:02:38.657509Z",
                    "pending_cancellation": False,
                    "customer": {
                        "id": "cus_PMkWepVUrSbG3gr1",
                        "name": "Alexandre",
                        "email": "amonteiro.sp@gmail.com",
                        "code": "09308007-332c-41f2-9642-1e3e0e7ac33b",
                        "document": "13100180810",
                        "type": "individual",
                        "delinquent": False,
                        "created_at": "2024-02-22T18:20:04.927Z",
                        "updated_at": "2024-02-22T18:20:04.927Z",
                        "birthdate": "1969-11-19T00:00:00Z",
                        "phones": {"mobile_phone": {"country_code": "55", "number": "98555880", "area_code": "11"}},
                        "metadata": {},
                    },
                    "last_transaction": {
                        "transaction_type": "pix",
                        "pix_provider_tid": "2379366004",
                        "qr_code": "00020101021226820014br.gov.bcb.pix2560pix.stone.com.br/pix/v2/cfc63d4c-8b48-4309-998e-994e6e49da6252040000530398654041.005802BR5925FanTicket Brasil Servicos6014RIO DE JANEIRO62290525paclsynvximtdmt1fk34cd4a0630409D0",
                        "qr_code_url": "https://api.pagar.me/core/v5/transactions/tran_6NXgVyh0VSr8EPAn/qrcode?payment_method=pix",
                        "end_to_end_id": "E31872495202402231302aGm4EXo2wyv",
                        "payer": {
                            "name": "ALEXANDRE RODRIGUES MONTEIRO DE SOUSA",
                            "document": "***001808**",
                            "document_type": "cpf",
                            "bank_account": {"bank_name": "Banco C6 S.A.", "ispb": "31872495"},
                        },
                        "expires_at": "2027-10-23T05:28:42Z",
                        "id": "tran_O6PzOmBSwTo5abk0",
                        "gateway_id": "2379366004",
                        "amount": 100,
                        "status": "paid",
                        "success": True,
                        "created_at": "2024-02-23T13:02:38.657509Z",
                        "updated_at": "2024-02-23T13:02:38.657509Z",
                        "gateway_response": {},
                        "antifraud_response": {},
                        "metadata": {},
                    },
                    "metadata": {},
                }
            ],
            "metadata": {},
        },
    }
    """

    id: str
    account: dict
    type: str
    created_at: str
    data: PagarmePaidWebhookData

    model_config = ConfigDict(from_attributes=True)


class FanTicketWebhookTicketData(BaseModel):
    unique_id: str
    is_paired: bool
    pair_unique_id: str | None = None
    is_reserved: bool
    is_sold: bool
    is_deleted: bool


class FanTicketWebhookProcessed(BaseModel):
    status: str
    user_uuid: str | None = None
    tickets_uuids_str: str | None = None
    tickets: list[FanTicketWebhookTicketData] | None = None

    model_config = ConfigDict(from_attributes=True)
