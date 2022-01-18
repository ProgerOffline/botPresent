#-*- coding: utf-8 -*-

from database import users_api
from database import settings_api


async def count_users_invest():
    constatns = await settings_api.get_constants()
    users = await users_api.get_all()
    
    if constatns != [] and users != []:
        for user in users:
            amount = user.invest_amount / 100 * constatns.precent
            amount = user.invest_amount + amount

            await users_api.set_invest_amount(user.user_id, round(amount, 2))