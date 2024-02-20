import re
import json
from typing import Optional
from urllib.parse import urljoin
from http import HTTPStatus
import requests
from pydantic import BaseModel, ValidationError

from app import schema as s
from app.logger import log

from config import BaseConfig
from .exceptions import (
    APIGetCustomerError,
    WrongUrlError,
    APIConnectionError,
    APICreateOrderError,
)

from config import config

CFG = config()


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

    # def create_order(self, order_data: s.PagarmeOrderCreateData) -> dict:
    #     response = self.api.post(self.__generate_url__("orders"), data=order_data.model_dump(exclude_none=True))
    #     return response.json()

    # def create_checkout_order(self, order_data: s.PagarmeOrderCreateData):
    #     for payment in order_data.payments:
    #         payment.payment_method = "checkout"

    #     return self.create_order(order_data)

    # def create_credit_card_order(self, order_data: s.PagarmeOrderCreateData):
    #     for payment in order_data.payments:
    #         payment.payment_method = "credit_card"

    #     return s.PagarmeCreateOrderOutput.model_validate(self.create_order(order_data))

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
        # Logging a request data to a file
        with open("pix_order_request.json", "w") as file:
            file.write(create_order_data.model_dump_json())

        response = self.api.post(self.__generate_url__("orders"), json=create_order_data.model_dump(exclude_none=True))

        # Logging a response data to a file
        try:
            with open("pix_order_response.json", "w") as file:
                file.write(json.dumps(response.json()))
        except Exception as e:
            log(log.ERROR, "Cannot save response logs to a file: [%s]", e)

        if response.status_code == HTTPStatus.FORBIDDEN:
            raise APIConnectionError
        try:
            response_data = s.PagarmeCreateOrderResponsePix.model_validate(response.json())
        except ValidationError:
            log(log.ERROR, "create_order response: [%s]", response.text)
            raise APICreateOrderError(response.text)

        return response_data

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
        # Regexp for phone validation
        match_res = re.search(CFG.PATTERN_PHONE, phone)
        country_code = match_res.group(1) if match_res else self.BRASIL_COUNTRY_PHONE_CODE
        area_code = match_res.group(2) if match_res else self.BRASIL_COUNTRY_AREA_CODE
        number = match_res.group(3) if match_res else phone
        return s.PagarmePhoneData(
            country_code=country_code,
            area_code=area_code,
            number=number,
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
