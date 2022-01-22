#-*- coding: utf-8 -*-

from quart import json
from loader import app
from quart import request
from database import payments_api


@app.route("/api/getPayments", methods=['GET'])
async def api_get_payments():
    payments = await payments_api.get_all()
    result_list = []

    for payment in payments:
        data = {
            "id" : payment.id,
            "user_db_id" : payment.user_db_id,
            "phone" : payment.phone,
            "date" : payment.date.strftime("%d.%m.%y %H:%M"),
            "bank" : payment.bank,
            "amount" : payment.amount,
            "status" : payment.status,
        }
        result_list.append(data)
    
    response = app.response_class(
        response=json.dumps(result_list),
        status=200,
        mimetype='application/json',
    ) 
    
    return response


@app.route("/api/delete/payment", methods=["POST"])
async def delet_payment():
    data = await request.form
    _id = int(data['id'])

    await payments_api.delete_payment(_id)

    response = app.response_class(
        response="",
        status=200,
    ) 

    return response