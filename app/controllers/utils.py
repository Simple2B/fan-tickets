from datetime import datetime, UTC
from flask import current_app as app
from app import models as m


def utcnow_chat_format():
    now = datetime.now(UTC)
    return now.strftime(app.config["DATE_CHAT_HISTORY_FORMAT"])


def get_tickets_fees(buyer: m.User, seller: m.User, global_fee_settings: m.GlobalFeeSettings):
    if buyer.is_authenticated and buyer.buyers_service_fee is not None:
        if seller.sellers_service_fee is not None:
            service_fee = buyer.buyers_service_fee + seller.sellers_service_fee
        else:
            service_fee = buyer.buyers_service_fee + global_fee_settings.service_fee_seller
    else:
        if seller.sellers_service_fee is not None:
            service_fee = global_fee_settings.service_fee_buyer + seller.sellers_service_fee
        else:
            service_fee = global_fee_settings.service_fee

    if buyer.is_authenticated and buyer.buyers_bank_fee is not None:
        if seller.sellers_bank_fee is not None:
            bank_fee = buyer.buyers_bank_fee + seller.sellers_bank_fee
        else:
            bank_fee = buyer.buyers_bank_fee + global_fee_settings.bank_fee_seller
    else:
        if seller.sellers_bank_fee is not None:
            bank_fee = global_fee_settings.bank_fee_buyer + seller.sellers_bank_fee
        else:
            bank_fee = global_fee_settings.bank_fee

    return service_fee, bank_fee
