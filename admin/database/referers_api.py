#-*- coding: utf-8 -*-

from database.models import Referers


async def create_record(referer_id, user_id) -> Referers:
    """
        Создает запись свзяи пользователя с рефералом
        args:
            referer_id - идентификатор телеграмма, реферала
            user_id - идентификатор телеграмма, пользователя
    """

    referer = await get_referer(user_id)
    if referer:
        return referer

    new_record = Referers()
    new_record.user_id = user_id
    new_record.referer_id = referer_id
    await new_record.create()
    return new_record


async def get_referer(user_id) -> Referers:
    """
        Возвращает идентификатор пользователя и реферала, 
        если они связаны. Если нет записи вернет None
        args:
            user_id - идентификатор телеграмма, пользователя
    """

    record = await Referers.query.where(
        Referers.user_id == user_id
    ).gino.first() 
    return record