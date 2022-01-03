#-*- coding: utf-8 -*-

from aiogram import types
from database import users_api
from logzero import logger
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext


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