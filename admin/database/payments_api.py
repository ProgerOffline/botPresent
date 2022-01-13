#-*- coding: utf-8 -*-

import widgets
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


async def update_payment(payment_data: dict) -> None:
    """
        Обновляет данные записи
        args:
            payment_data - словарь новых данных 
    """

    payment = await get_payment(payment_data['id'])
    await payment.update(
        phone=payment_data['phone'],
        date=payment_data['date'],
        bank=payment_data['bank'],
        amount=payment_data['amount'],
        status=payment_data['status'],
    ).apply()


async def check_payment(payment_id : int) -> None:
    """
        Проверяет статус начисления денег на баланс пользователя
        args:
            payment_id - id записи о пополнении
    """
    payment = await get_payment(payment_id)

    if payment.status in  ("Начислено", "начислено") :
        user = await users_api.get_user_db_id(payment.user_db_id)

        await users_api.set_ballance(
            user_id=user.user_id, 
            amount=user.ballance + payment.amount,
        )
        await widgets.send_message(
            user_id=user.user_id,
            text=f"ℹ️ На ваш баланс успешно зачислено {payment.amount} руб.",
        )
        await set_status(payment_id, "Выполнен")
    
    elif payment.status in ("Отмена", "отмена"):
        user = await users_api.get_user_db_id(payment.user_db_id)

        await widgets.send_message(
            user_id=user.user_id,
            text=f"❌ Ваш платеж на сумму {payment.amount}, был отклонён " + \
                "Администратором.",
        )
        await set_status(payment_id, "Отменен")