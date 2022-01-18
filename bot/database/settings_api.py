#-*- coding: utf-8 -*-

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
        wallet_pm=constants_data['wallet_pm'],
        pm_account=constants_data['pm_account'],
        pm_passwd=constants_data['pm_passwd'],
    ).apply()