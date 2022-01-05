#-*- coding: utf-8 -*-

from logzero import logger
from callbacks import corres
from database.models import Support
from database.users_api import get_user


async def create_corres(user_id, quest_type, quest_full, msg_id) -> Support:
    """
        Создает переписку с тех. поддержкой
        args:
            user_id - id пользователя в телеграмме
            quest_type - тип вопроса
            quest_full - полный, развернутый вопрос
    """

    new_corres = Support()
    new_corres.user_id = user_id
    new_corres.support_id = 0
    new_corres.quest_type = quest_type
    new_corres.quest_full = quest_full
    new_corres.msg_id = 0

    await new_corres.create()
    return new_corres


async def get_corres(corres_id) -> Support:
    """
        Возвращает данные переписки
        args:
            id - Уникальный идентификатор переписки
    """

    corres = await Support.query.where(Support.id == corres_id).gino.first()
    return corres


async def set_support_id(corres_id, user_id) -> None:
    """
        Устанавливает в качестве собеседника тех поддержку
        agrs:
            corres_id - идентификатор переписки
            user_id - id пользователя в телеграмме
    """

    corres = await get_corres(corres_id)
    await corres.update(support_id=user_id).apply()


async def set_msg_id(corres_id, msg_id) -> None:
    """
        Устанавливает новый идентификатор сообщения, 
        которое было отправлено в чат поддержки
        args:
            corres_id - идентификатор переписки
            msg_id - идентификатор сообщения
    """

    corres = await get_corres(corres_id)
    await corres.update(msg_id=msg_id).apply()