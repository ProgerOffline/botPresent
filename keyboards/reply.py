#-*- coding: utf-8 -*-

from logzero import logger
from aiogram import types



def authorization():
    logger.info("Get authorization keyboard")

    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).add(
        types.KeyboardButton(
            text="Регистрация",
            request_contact=True,
        ),
        types.KeyboardButton(
            text="Войти",
            request_contact=True,
        ),
    )