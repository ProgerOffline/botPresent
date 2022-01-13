#-*- coding: utf-8 -*-

from datetime import datetime

from database.models import UsersPayments
from database import users_api


async def get_payment(payment_id) -> UsersPayments:
    """
        Возвращает запись о пополнении
        args:
            payment_id - id записи
    """

    payment = await UsersPayments.query.where(
        UsersPayments.id == payment_id
    ).gino.first()

    return payment


async def get_all() -> list:
    """
        Возвращает список все записей о пополнении
    """

    payments = await UsersPayments.query.gino.all()
    return payments


async def set_status(payment_id, status) -> None:
    """
        Устанавливает новый статус для записи
        args:
            payment_id - id записи
            status - новый статус
    """

    payment = await get_payment(payment_id)
    await payment.update(status=status).apply()


async def add_payment(user_id, bank, amount) -> UsersPayments:
    """
        Создает новую запись о пополнении
        args:
            user_id - id пользователя в телеграмме
            bank - название банка через которого было осуществлено пополнение
            amount - сумма пополнения
    """
    
    user = await users_api.get_user(user_id)
    new_payment = UsersPayments()
    new_payment.user_db_id = user.id
    new_payment.phone = user.phone
    new_payment.date = datetime.now()
    new_payment.wallet = user.wallet
    new_payment.bank = bank
    new_payment.amount = amount
    new_payment.status = "-"
    new_payment.client_status = "-"
    await new_payment.create()
    
    return new_payment


async def set_client_status(payment_id, status) -> None:
    """
        Устанавливает статус для баланса клиента
        args:
            payment_id - id записи
            status - новый статус
    """

    payment = await get_payment(payment_id)
    await payment.update(status=status).apply()