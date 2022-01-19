#-*- coding: utf-8 -*-

from datetime import datetime
from quart import request
from database import users_api, payments_api, settings_api
from loader import app


@app.route("/api/save/clients", methods=['POST'])
async def save_clients():
    data = await request.form
    data = eval(data['new-data'])

    for i in data:
        reg_date = [int(i) for i in data[i][2].split(".")]
        reg_date = datetime(reg_date[2], reg_date[1], reg_date[0])
        user = {
            "user_id" : int(data[i][0]),
            "phone" : int(data[i][1]),
            "reg_date" : reg_date,
            "wallet" : data[i][3],
            "ballance" : int(data[i][4]),
            "invest_amount" : int(data[i][5]),
        }
        await users_api.update_user(user)

    response = app.response_class(
        response="",
        status=200,
    )
    return response


@app.route("/api/save/payments", methods=['POST'])
async def save_payments():
    data = await request.form
    data = eval(data['new-data'])

    for i in data:
        date = data[i][2].split(" ")
        time = [int(i) for i in date[1].split(":")]
        date = [int(i) for i in date[0].split(".")]
        date = datetime(date[2], date[1], date[0], hour=time[0], minute=time[1])

        payment = {
            "id" : int(data[i][0]),
            "phone" : int(data[i][1]),
            "date" : date,
            "bank" : data[i][3],
            "amount" : int(data[i][4]),
            "status" : data[i][5],
        }
        await payments_api.update_payment(payment)
        await payments_api.check_payment(payment['id'])

    response = app.response_class(
        response="",
        status=200,
    )
    return response


@app.route("/api/save/settings", methods=["POST"])
async def save_settings():
    data = await request.form
    data = eval(data['new-data'])['0']

    constants = {
        "precent" : float(data[0]),
        "cber_bank" : int(data[1]),
        "tinkoff_bank" : int(data[2]),
        "fio_cber" : data[3],
        "fio_tinkoff" : data[4],
        "wallet_pm" : data[5],
        "pm_account" : int(data[6]),
        "pm_passwd" : data[7],
    }
    # TODO: Возможно понадобиться, пока оставлю здесь
    # await settings_api.check_precent(constants)
    
    await settings_api.update_constants(constants)
    
    response = app.response_class(
        response="",
        status=200,
    )
    return response