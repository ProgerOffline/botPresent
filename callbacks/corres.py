#-*- coding: utf-8 -*-

from aiogram import types
from aiogram.dispatcher import FSMContext
from callbacks import ctypes

def setup(dp):
    @dp.callback_query_handler(ctypes.corres.filter(type="answer"))
    async def corres_answer(call: types.Message, state: FSMContext):
        pass