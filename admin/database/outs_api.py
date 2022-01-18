#-*- coding: utf-8 -*-

from database.models import OutsRecords
from database import users_api
from datetime import datetime


async def get_record(record_id : int) -> OutsRecords:
    """
        Возвращает запись о выводе средств
        args:
            record_id - id записи
    """

    record = await OutsRecords.query.where(
        OutsRecords.id == record_id
    ).gino.first()
    return record


async def add_record(user_id : int, amount: float, status : str) -> None:
    """
        Создает запись о выводе средств
        args:
            user_id - id пользователя в базе данных
            amount - сумма вывода
            status - статус перевода
    """

    user = await users_api.get_user_db_id(user_id)
    record = OutsRecords()
    record.user_db_id = user.id
    record.phone = user.phone
    record.date = datetime.now()
    record.wallet = user.wallet
    record.amount = amount
    record.status = status
    await record.create()


async def get_all() -> list:
    """
        Возвращает список всех записей о пополнении
    """

    records = await OutsRecords.query.gino.all()
    return records