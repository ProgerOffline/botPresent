#-*- coding: utf-8 -*-

import keyboards

from aiogram import types
from logzero import logger
from database import users_api


def setup(dp):
    # Пользователь отправил свой контакт
    @dp.message_handler(content_types="contact", is_sender_contact=True)
    async def login_in(message: types.Message):
        logger.info(f"{message.from_user.id} : sent my contact")
        contact = types.Contact()
        contact.user_id = message.from_user.id
        contact.phone_number = int(message.contact.phone_number)
        contact.first_name = message.from_user.username

        await users_api.add_new_user(contact)
        await message.answer(
            text="💻 Добро пожаловать в личный кабинет",
            reply_markup=keyboards.reply.main_menu(),
        )