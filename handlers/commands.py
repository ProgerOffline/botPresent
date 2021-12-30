#-*- coding: utf-8 -*-

import keyboards
from aiogram import types


def setup(dp):
    @dp.message_handler(commands=['start'])
    async def commands(message: types.Message):
        await message.answer(
            text=" 👋 Добро пожаловать в чат бот компании OKO",
            reply_markup=keyboards.reply.authorization(),
        )