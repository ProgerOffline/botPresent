#-*- coding: utf-8 -*-

from quart import json
from loader import app
from database import outs_api


@app.route("/api/getOuts")
async def get_outs():
    outs_records = await outs_api.get_all()
    result_list = []

    for record in outs_records:
        record.error = "Нет ошибок" if record.error == None else record.error 
        data = {
            "id" : record.user_db_id,
            "phone" : record.phone,
            "date" : record.date.strftime("%d.%m.%y %H:%M"),
            "wallet" : record.wallet,
            "amount" : record.amount,
            "error" : record.error,
        }
        result_list.append(data)
    
    response = app.response_class(
        response=json.dumps(result_list),
        status=200,
        mimetype="application/json",
    )

    return response