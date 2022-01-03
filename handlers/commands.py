#-*- coding: utf-8 -*-

import keyboards
from database.models import DBCommands
from aiogram import types
from aiogram.dispatcher import FSMContext

db = DBCommands()

def setup(dp):
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message, state="*"):
        await message.answer(
            text=" 👋 Добро пожаловать в чат бот компании OKO",
            reply_markup=keyboards.reply.authorization(),
        )
    
    @dp.message_handler(commands=['show'])
    async def cmd_show(message: types.Message):
        users = await db.get_all_users()
        print(users)
        await message.answer(
            text=[
                f"{user.id} : {user.user_id}: {user.phone}"
                for user in users
            ],
        )     
