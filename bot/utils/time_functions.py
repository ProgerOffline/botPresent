#-*- coding: utf-8 -*-

from database import users_api
from database import settings_api


async def count_users_invest(bot):
    constatns = await settings_api.get_constants()
    users = await users_api.get_all()
    
    if constatns != [] and users != []:
        for user in users:
            dividends = user.invest_amount / 100 * constatns.precent
            amount = user.ballance + dividends

            await users_api.set_ballance(user.user_id, round(amount, 2))
            await bot.send_message(
                chat_id=user.user_id, 
                text=f"💵Прибыль за последние 24 часа составила {dividends}",
            )
