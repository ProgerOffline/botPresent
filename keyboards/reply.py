#-*- coding: utf-8 -*-

from logzero import logger
from aiogram import types



def authorization(in_base):
    """
    Возвращает одну кнопку входа, если пользователь есть в базе
    То текст будет "Войти", если нет в базе тогда "Регистрация"
    agrs:
        in_base - Наличие пользователя в базе
    """
    logger.info("Get authorization keyboard")

    if in_base:     
        return types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=1,
        ).add(
            types.KeyboardButton(
                text="Войти",
                request_contact=True,
            ),
        )
    else:
        return types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=1,
        ).add(
            types.KeyboardButton(
                text="Регистрация",
                request_contact=True,
            ),
        )