#-*- coding: utf-8 -*-

from database.models import Settings


async def get_constants() -> Settings:
    """
        Возвращает объект всех констант
    """

    constants = await Settings.query.gino.first()
    return constants