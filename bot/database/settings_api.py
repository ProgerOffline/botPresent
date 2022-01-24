#-*- coding: utf-8 -*-

from database.models import Settings


async def get_constants() -> Settings:
    """
        Возвращает объект всех констант
    """

    constants = await Settings.query.where(Settings.id == 1).gino.first()
    return constants