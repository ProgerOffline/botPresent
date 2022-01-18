#-*- coding: utf-8 -*-

import widgets
from database.models import Settings


async def get_constants() -> Settings:
    """
        Возвращает объект всех констант
    """

    constants = await Settings.query.gino.first()
    return constants


async def update_constants(constants_data: dict) -> None:
    """
        Обновляет данные констант
    """

    constants = await get_constants()
    await constants.update(
        precent=constants_data['precent'],
        cber_bank=constants_data['cber_bank'],
        tinkoff_bank=constants_data['tinkoff_bank'],
        fio=constants_data['fio'],
        wallet_pm=constants_data['wallet_pm'],
        pm_account=constants_data['pm_account'],
        pm_passwd=constants_data['pm_passwd'],
    ).apply()


async def check_precent(constants_data: dict) -> None:
    """
        Проверяет изменен ли процент
    """

    constants = await get_constants()
    if constants.precent != constants_data['precent']:
        await widgets.send_all(
            text="💵Прибыль за последние 24 часа " + \
                f"составила {constants_data['precent']}%"
        )
