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
        "wallet_pm" : constants.wallet_pm,
    }

    response = app.response_class(
        response=json.dumps(data),
        status=200,
    )
    return response