#-*- coding: utf-8 -*-

from logzero import logger
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from database import users_api


class UpdateLoggerMiddleware(BaseMiddleware):
    async def on_process_update(self, update: types.Update, data: dict):
        logger.info(update)

        user = await users_api.get_user(update.message.from_user.id)
        if user != None:
            if not user.permission:
                print(f"User is blocked: {update.message.from_user.id}")
                raise CancelHandler()
            
        elif '/start' in update.message.text:
            pass
        
        elif user == None:
            await update.message.answer(
                text="⚠️ Ошибка: Что-то пошло не так, попробуйте нажать /start",
                reply_markup=types.ReplyKeyboardRemove(),
            )

            raise CancelHandler()
