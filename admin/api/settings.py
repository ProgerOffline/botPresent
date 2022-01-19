#-*- coding: utf-8 -*-

from quart import json
from loader import app
from database import settings_api


@app.route("/api/getConstants")
async def get_constants():
    constants = await settings_api.get_constants()
    data = {
        "precent" : constants.precent,
        "cber_bank" : constants.cber_bank,
        "tinkoff_bank" : constants.tinkoff_bank,
        "fio_cber" : constants.fio_cber,
        "fio_tinkoff" : constants.fio_tinkoff,
        "wallet_pm" : constants.wallet_pm,
        "pm_account" : constants.pm_account,
        "pm_passwd" : constants.pm_passwd,
        "support_chat_id" : constants.support_chat_id,
    }

    response = app.response_class(
        response=json.dumps(data),
        status=200,
    )
    return response