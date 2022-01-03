#-*- coding: utf-8 -*-

from aiogram import types
from logzero import logger

from database.models import User


async def get_user(user_id) -> User:
    """
        Получаем пользователя из базы
        args:
            user_id - id пользователя в телеграмме
    """
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user
    

async def add_new_user(contact) -> User: 
    """
        Добавляем пользователя в базу если его в ней нет
        args:
            contact - types.Contact (контакт пользователя)
    """
    old_user = await get_user(contact.user_id)
    
    if old_user:
        return old_user
    
    logger.info(f"Add new user: {contact.user_id}, {contact.phone_number}")
    new_user = User()
    new_user.user_id = contact.user_id
    new_user.phone = contact.phone_number
    new_user.username = contact.first_name

    await new_user.create()
    return new_user


async def get_all_users() -> list:
    """
        Получаем всех пользователей
        args:
            none
    """
    users = await User.query.gino.all()
    return users
