#-*- coding: utf-8 -*-

from aiogram import types
from logzero import logger
from callbacks import ctypes


def answer(corres_id):
    logger.info("Get answer keyboard")

    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            text="✏️ Ответить",
            url=f"https://t.me/tg4bot_bot?start=answer_{corres_id}",
        ),
    ) 