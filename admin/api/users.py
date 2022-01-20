#-*- coding: utf-8 -*-

from quart import json
from loader import app
from database import users_api, payments_api


@app.route("/api/getUsers", methods=['GET'])
async def api_get_users():
    users = await users_api.get_all()
    result_list = []

    for user in users:
        permission = "Открыт" \
            if user.permission \
            else "Закрыт"

        username = user.username \
            if user.username != None \
            else "-" 

        data = {
            "id" : user.id,
            "user_id" : user.user_id,
            "username" : username,
            "phone" : user.phone,
            "ballance" : user.ballance,
            "buyed" : user.buyed,
            "invest_amount" : user.invest_amount,
            "wallet" : user.wallet,
            "referer" : user.referer,
            "ref_level" : user.ref_level,
            "reg_date" : user.reg_date.strftime("%d.%m.%y"),
            "permission" : permission,
        }
        result_list.append(data)

    response = app.response_class(
        response=json.dumps(result_list),
        status=200,
        mimetype='application/json',
    ) 

    return response