#-*- coding: utf-8 -*-

from quart import json
from loader import app
from database import users_api


@app.route("/api")
async def api_index():
    pass


@app.route("/api/getUsers")
async def api_get_users():
    users = await users_api.get_all()
    users_list = []

    for user in users:
        data = {
            "id" : user.id,
            "user_id" : user.user_id,
            "username" : user.username,
            "phone" : user.phone,
            "ballance" : user.ballance,
            "buyed" : user.buyed,
            "invest_amount" : user.invest_amount,
            "wallet" : user.wallet,
            "referer" : user.referer,
            "ref_level" : user.ref_level,
            "reg_date" : user.reg_date,
        }
        users_list.append(data)

    response = app.response_class(
        response=json.dumps(users_list),
        status=200,
        mimetype='application/json',
    ) 

    return response