#-*- coding: utf-8 -*-

import os

from datetime import datetime
from quart import request
from werkzeug.utils import secure_filename
from database import users_api, payments_api, settings_api
from loader import app


@app.route("/api/save/clients", methods=['POST'])
async def save_clients():
    data = await request.form
    data = eval(data['new-data'])

    for i in data:
        reg_date = [int(i) for i in data[i][3].split(".")]
        reg_date = datetime(reg_date[2], reg_date[1], reg_date[0])
        user = {
            "user_id" : int(data[i][0]),
            "phone" : int(data[i][2]),
            "reg_date" : reg_date,
            "wallet" : data[i][4],
            "ballance" : int(data[i][5]),
            "invest_amount" : int(data[i][6]),
        }
        await users_api.update_user(user)
        await users_api.check_user_block(data[i][7], user['user_id'])

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
        phone = int(data[i][1]) \
            if data[i][1] != "null" \
            else 0

        date = data[i][2].split(" ")
        time = [int(i) for i in date[1].split(":")]
        date = [int(i) for i in date[0].split(".")]
        date = datetime(date[2], date[1], date[0], hour=time[0], minute=time[1])

        payment = {
            "user_db_id" : int(data[i][0]),
            "phone" : phone,
            "date" : date,
            "bank" : data[i][3],
            "amount" : int(data[i][4]),
            "status" : data[i][5],
            "id" : int(data[i][7]),
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
        "support_chat_id" : int(data[8]),
    }

    change_precent = await settings_api.check_precent(constants)

    if change_precent:
        try:
            path = os.getcwd() + "/precentPicture"
            os.remove(path)
        except FileNotFoundError:
            pass

    await settings_api.update_constants(constants)
    
    response = app.response_class(
        response="",
        status=200,
    )
    return response


@app.route("/api/save/picture", methods=["POST"])
async def save_picture():
    picture = await request.files
    
    if str(picture) != "ImmutableMultiDict([])":
        flag = True
        while flag:
            picture = picture['file']
            await picture.save(secure_filename("precentPicture"))

            try:
                path = os.getcwd() + "/precentPicture"
                image = open(path)
                flag = False
            except:
                pass

    response = app.response_class(
        response="",
        status=200,
    )
    return response