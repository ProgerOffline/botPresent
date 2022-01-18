#-*- coding: utf-8 -*-

from database.models import User
from datetime import datetime

async def get_user(user_id) -> User:
    """
        Получает пользователя из базы
        args:
            user_id - id пользователя в телеграмме
    """

    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def get_user_db_id(user_id) -> User:
    """
        Возвращает пользователя из базы
        args:
            user_id - id пользователя из базы данных
    """

    user = await User.query.where(User.id == user_id).gino.first()
    return user
    

async def add_new_user(contact, referer=0) -> User: 
    """
        Добавляет пользователя в базу если его в ней нет
        args:
            contact - types.Contact (контакт пользователя)
    """

    old_user = await get_user(contact.user_id)
    
    if old_user:
        return old_user
    
    new_user = User()
    new_user.user_id = contact.user_id
    new_user.phone = contact.phone_number
    new_user.username = contact.first_name
    new_user.ballance = 0.0
    new_user.buyed = False
    new_user.invest_amount = 0
    new_user.wallet = "Не указан"
    new_user.referer = referer
    new_user.ref_level = 3
    new_user.reg_date = datetime.now()

    await new_user.create()
    return new_user


async def set_ballance(user_id, amount) -> None:
    """
        Устанавливает новый баланс для пользователя
        args:
            user_id - id пользователя в телеграмме
            amount - сумма нового баланса
    """

    user = await get_user(user_id)
    await user.update(ballance=amount).apply()


async def set_wallet(user_id, wallet) -> None:
    """
        Устанавливает новый кошелек
        args:
            user_id - id пользователя в телеграмме
            wallet - номер кошелька perfect money
    """

    user = await get_user(user_id)
    await user.update(wallet=wallet).apply()


async def set_invest_amount(user_id, amount) -> None:
    """
        Устанавливает новую сумму инвестиции
        args:
            user_id - id пользователя в телеграмме
            amount - сумма нового баланса
    """

    user = await get_user(user_id)
    await user.update(invest_amount=amount).apply()


async def get_all() -> list:
    """
        Возвращает список всех зарегистрированных пользователей
    """

    users = await User.query.gino.all()
    return users