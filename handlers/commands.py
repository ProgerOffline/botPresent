#-*- coding: utf-8 -*-

import keyboards 
from database import users_api
from aiogram import types
from aiogram.dispatcher import FSMContext


def setup(dp):
    # Приветственное сообщение
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message, state="*"):
        is_base = bool(await users_api.get_user(message.from_user.id))

        await message.answer(
            text=" 👋 Добро пожаловать в чат бот компании OKO",
            reply_markup=keyboards.reply.authorization(is_base),
        )
    
    # Вывод всех пользователей, зарегистрированных в боте
    @dp.message_handler(commands=['show'])
    async def cmd_show(message: types.Message):
        users = await users_api.get_all_users()
        await message.answer(
            text=[
                f"{user.id} : {user.user_id} : {user.username} : {user.phone}"
                for user in users
            ],
        )     
