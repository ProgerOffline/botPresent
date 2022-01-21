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


async def create_record_user(user_id, affiliate_id) -> User:
    """
        Возвращает первичную запись о пользователе
        args:
            user_id - id пользователя в телеграмме
            affiliate_id - id аффилиала в телеграмме
    """
    
    record_user = User()
    record_user.user_id = user_id
    record_user.affiliate = affiliate_id
    record_user.referers = []
    record_user.permission = True
    await record_user.create()

    return record_user


async def add_new_user(contact) -> User: 
    """
        Добавляет пользователя в базу если его в ней нет
        args:
            contact - types.Contact (контакт пользователя)
    """

    user = await get_user(contact.user_id)
    if not user.phone:
        await user.update(
            phone=contact.phone_number,
            username=contact.first_name,
            ballance=0.0,
            invest_amount=0,
            wallet="Не указан",
            reg_date=datetime.now(),
        ).apply()

    return user


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


async def set_invest_time(user_id: int) -> None:
    """
        Устанавливает время покупки инвестиции на текущее
        args:
            user_id - id пользователя в телеграмме
    """

    hours = datetime.now().hour
    user = await get_user(user_id)
    await user.update(invest_time=hours).apply()


async def set_affiliate(referal_id, affiliate_id) -> None:
    """
        Устанавливает аффилиал для реферала
        args:
            referal_id - id реферала в телеграмме
            affiliate_id - id аффилиала в телеграмме
    """

    referal = await get_user(referal_id)
    await referal.update(affiliate=affiliate_id).apply()


async def add_referal(affiliate_id, referal_id) -> None:
    """
        Добавляет реферала в список рефералов аффилиала
        args:
            affiliate_id - id аффилиала в телеграмме
            referal_id - id реферала в базе данных
    """

    affiliate = await get_user(affiliate_id)
    _list = affiliate.referers
    _list.append(referal_id)

    await affiliate.update(
        referers=_list,
    ).apply()