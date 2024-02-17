from typing import Optional
from urllib.parse import urljoin
from http import HTTPStatus
import requests
from pydantic import BaseModel, ValidationError

from app import schema as s, models as m
from app.logger import log

from config import BaseConfig
from .exceptions import (
    APIGetCustomerError,
    WrongUrlError,
    APIConnectionError,
    APICreateOrderError,
)


class PagarmeClient:
    BRASIL_COUNTRY_PHONE_CODE: str
    BRASIL_COUNTRY_AREA_CODE: str
    PAGARME_CHECKOUT_EXPIRES_IN: int
    PAGARME_DEFAULT_PAYMENT_METHOD: str
    PAGARME_WEBHOOK_URL: str

    http_headers: dict
    base_url: str
    api: requests.Session

    def __init__(self):
        self.http_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "",
        }

        self.api = requests.Session()

    def __generate_url__(self, path: str, query_params: Optional[BaseModel] = None) -> str:
        url = urljoin(self.base_url, path)
        if not query_params:
            return url

        request = requests.models.PreparedRequest()
        request.prepare_url(url, query_params.model_dump(exclude_none=True))

        if not request.url:
            raise WrongUrlError(self.base_url, path, query_params.model_dump(exclude_none=True))

        return request.url

    def configure(self, config: BaseConfig):
        self.BRASIL_COUNTRY_PHONE_CODE = config.BRASIL_COUNTRY_PHONE_CODE
        self.BRASIL_COUNTRY_AREA_CODE = config.BRASIL_COUNTRY_AREA_CODE
        self.PAGARME_CHECKOUT_EXPIRES_IN = config.PAGARME_CHECKOUT_EXPIRES_IN
        self.PAGARME_DEFAULT_PAYMENT_METHOD = config.PAGARME_DEFAULT_PAYMENT_METHOD
        self.PAGARME_WEBHOOK_URL = config.PAGARME_WEBHOOK_URL
        self.PAGARME_SELLER_PERCENTAGE = config.PAGARME_SELLER_PERCENTAGE
        self.PAGARME_PLATFORM_PERCENTAGE = config.PAGARME_PLATFORM_PERCENTAGE
        self.PAGARME_DEFAULT_FT_CUSTOMER_ID = config.PAGARME_DEFAULT_FT_CUSTOMER_ID
        self.PAGARME_DEFAULT_FT_RECIPIENT_ID = config.PAGARME_DEFAULT_FT_RECIPIENT_ID

        self.base_url = config.PAGARME_BASE_URL

        self.http_headers["authorization"] = f"Basic {config.PAGARME_SECRET_KEY}"
        self.api.headers.update(self.http_headers)

    def get_orders(self, query: Optional[s.PagarmePaginationQuery] = None):
        response = self.api.get(self.__generate_url__("orders", query))
        return response.json()

    def get_order(self, order_id: str) -> Optional[s.PagarmeOrderOut]:
        url = urljoin(f"{self.__generate_url__('orders')}/", order_id)
        response = self.api.get(url)

        if response.status_code != HTTPStatus.OK:
            return None

        return s.PagarmeOrderOut.model_validate(response.json())

    def create_order(self, order_data: s.PagarmeCreateOrderInput):
        response = self.api.post(self.__generate_url__("orders"), json=order_data.model_dump(exclude_none=True))
        return s.PagarmeCreateOrderOutput.model_validate(response.json())

    def generate_checkout_data(
        self, card_input: s.PagarmeCardInput, billing_address_editable=False, customer_editable=False
    ):
        return s.PagarmeCheckout(
            expires_in=self.PAGARME_CHECKOUT_EXPIRES_IN,
            payment_method=self.PAGARME_DEFAULT_PAYMENT_METHOD,
            billing_address_editable=billing_address_editable,
            customer_editable=customer_editable,
            accepted_payment_methods=[self.PAGARME_DEFAULT_PAYMENT_METHOD],
            success_url=self.PAGARME_WEBHOOK_URL,
            credit_card=card_input,
        )

    def create_order_pix(self, create_order_data: s.PagarmeCreateOrderPix):
        response = self.api.post(self.__generate_url__("orders"), json=create_order_data.model_dump(exclude_none=True))
        if response.status_code == HTTPStatus.FORBIDDEN:
            raise APIConnectionError
        try:
            response_data = s.PagarmeCreateOrderResponsePix.model_validate(response.json())
        except ValidationError:
            log(log.ERROR, "create_order response: [%s]", response.text)
            raise APICreateOrderError(response.text)

        return response_data

    def generate_split_data(self, ticket: m.Ticket):
        """
        data = {
            "items": [
                {
                    "amount": ticket.price_net * 100,
                    "description": f"Ticket {ticket.event.name}",
                    "quantity": 1,
                    "category": f"Ticket: {ticket.event.category.name}",
                }
            ],
            "customer_id": "cus_LD8jWxauYfOm9yEe",  # this is a default customer that pays from FT to sellers
            "payments": [
                "payment_method": "pix",
                {
                    "amount": 70,
                    "recipient_id": ticket.seller.recipient_id,
                    "type": "percentage",
                }
            ],
        }
        """

        data = s.PagarmeCreateOrderSplit(
            items=[
                s.PagarmeItem(
                    amount=ticket.price_net * 100,
                    description=f"Ticket {ticket.event.name}",
                    quantity=1,
                    category=ticket.ticket_category,
                )
            ],
            customer_id=self.PAGARME_DEFAULT_FT_CUSTOMER_ID,  # this is a default customer that pays from FT to sellers
            payments=[
                s.PagarmePaymentSplit(
                    payment_method="pix",
                    pix=s.PagarmePaymentPix(
                        expires_in=30,
                        payment_method="pix",
                        billing_address_editable=False,
                        customer_editable=False,
                        accepted_payment_methods=["pix"],
                        success_url="https://fan-ticket.simple2b.org/pay/webhook",
                        Pix=s.PagarmePixData(
                            expires_in=2147483647,
                        ),
                    ),
                    split=[
                        s.PagarmeSplitObject(
                            amount=self.PAGARME_SELLER_PERCENTAGE,  # 94% of the ticket price - has to be calculated according to new business rules
                            recipient_id=ticket.seller.recipient_id,
                            options=s.SplitOptions(),
                        ),
                        s.PagarmeSplitObject(
                            amount=self.PAGARME_PLATFORM_PERCENTAGE,  # 6% of the ticket price - has to be calculated according to new business rules
                            recipient_id=ticket.seller.recipient_id,
                            options=s.SplitOptions(),
                        ),
                    ],
                ),
            ],
        )

        return data

    def create_split(self, create_split_order_data: s.PagarmeCreateOrderSplit):
        """
        Split payment method is used as a 2nd stage of payment
        1st stage is when a buyer pays for a ticket to FanTicket platform via PIX payment method
        2nd stage is when FanTicket platform pays to the seller via split payment method
        On this stage split is used to pay to the seller, that is called on pagarme as recipient
        All the money that is paid to the FanTicket platform is redirected to the seller
        excluding the platform fee and the payment method fee, which are left on the platform account
        """

        response = self.api.post(
            self.__generate_url__("orders"),
            json=create_split_order_data.model_dump(exclude_none=True),
        )
        return response

    # Recipients for split payments
    def get_recipients(self):
        """
        Get all recipients from pagarme account.
        Recipients are the sellers that will receive the money from the FT on the 2nd stage.
        It's special role that is only in split payment method.
        """
        response = self.api.get(self.__generate_url__("recipients"))
        return response.json()

    def get_recipient(self, recipient_id: str):
        """Gets a single recipient by its id while split payment method is used."""
        response = self.api.get(self.__generate_url__(f"recipients/{recipient_id}"))
        return response.json()

    def prepare_recipient_data(self, ticket: m.Ticket) -> s.PagarmeRecipientCreate:
        name = f"{ticket.seller.name} {ticket.seller.last_name}"
        recipient_data = s.PagarmeRecipientCreate(
            name=name,
            email=ticket.seller.email,
            description="FanTicket platform seller",
            document=ticket.seller.document_identity_number,
            type="individual",
            code=ticket.seller.uuid,
            default_bank_account=s.DefaultBankAccount(
                holder_name=name,
                bank=ticket.seller.bank,
                branch_check_digit=ticket.seller.branch_check_digit,
                branch_number=ticket.seller.branch_number,
                account_number=ticket.seller.account_number,  # 16 digits
                account_check_digit=ticket.seller.account_check_digit,
                holder_type="individual",
                holder_document=ticket.seller.document_identity_number,
                type="checking",
            ),
        )
        return recipient_data

    def create_recipient(self, recipient_data: s.PagarmeRecipientCreate, seller: m.User):
        """Creates a recipient for split payment method."""
        response = self.api.post(self.__generate_url__("recipients"), json=recipient_data.model_dump())
        seller.recipient_id = response.json().get("id")
        return seller.recipient_id

    def check_recipient_credentials(self, seller: m.User) -> bool:
        if (
            seller.recipient_id
            and seller.bank
            and seller.branch_check_digit
            and seller.branch_number
            and seller.account_number
            and seller.account_check_digit
        ):
            return True
        return False

    # Customers
    def get_customers(
        self, customer_list_query: Optional[s.PagarCustomerListQuery] = None
    ) -> s.PagarCustomerListResponse:
        response = self.api.get(self.__generate_url__("customers", customer_list_query))
        if response.status_code != HTTPStatus.OK:
            raise APIGetCustomerError()

        return s.PagarCustomerListResponse.model_validate(response.json())

    def get_customer(self, customer_id: str) -> s.PagarmeCustomerOutput | None:
        response = self.api.get(self.__generate_url__(f"customers/{customer_id}"))

        if response.status_code != HTTPStatus.OK:
            log(log.ERROR, "get_customer [%s] response: [%s]", customer_id, response.text)
            return None

        return s.PagarmeCustomerOutput.model_validate(response.json())

    def create_customer(self, customer_data: s.PagarmeCustomerCreate):
        response = self.api.post(self.__generate_url__("customers"), json=customer_data.model_dump(exclude_none=True))

        print(response.status_code)
        if response.status_code != HTTPStatus.OK:
            log(log.ERROR, "create_pagarme_customer response: [%s]", response.text)
            return None
        log(log.INFO, "create_pagarme_customer response: [%s]", response.text)

        return s.PagarmeCustomerOutput.model_validate(response.json())

    def generate_customer_phone(self, phone: str):
        return s.PagarmePhoneData(
            country_code=self.BRASIL_COUNTRY_PHONE_CODE, area_code=self.BRASIL_COUNTRY_AREA_CODE, number=phone
        )

    # Cards
    def get_customer_card(self, customer_id: str, card_id: str) -> s.PagarmeCardOutput:
        response = self.api.post(self.__generate_url__(f"customers/{customer_id}/cards/{card_id}"))
        # TODO check for errors
        return s.PagarmeCardOutput.model_validate(response.json())

    def get_customer_cards(self, customer_id: str):
        response = self.api.get(self.__generate_url__(f"customers/{customer_id}/cards"))
        return response.json()

    def create_customer_card(self, card_data: s.PagarmeCardCreate):
        response = self.api.post(
            self.__generate_url__(f"customers/{card_data.customer_id}/cards"),
            json=card_data.model_dump(exclude_none=True),
        )
        # TODO check for errors
        log(log.INFO, "create_pagarme_card response: [%s]", response.text)
        print("-------")
        print(response.json())
        return s.PagarmeCardOutput.model_validate(response.json())
