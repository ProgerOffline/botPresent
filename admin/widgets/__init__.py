#-*- coding: utf-8 -*-

import aiohttp
import requests
from data.config import BOT_TOKEN
from database import users_api


async def send_message(user_id, text):
    """
        Оправляет сообщение через бота, юзеру
    """

    url = "https://api.telegram.org/bot" + BOT_TOKEN
    url += "/sendMessage"
    data = {
        "chat_id" : user_id,
        "text" : text,
    }
    async with aiohttp.ClientSession() as session:
        await session.get(url, params=data)


async def send_all(text):
    """
        Оправляет сообщение через бота, всем пользователям
    """
    
    users = await users_api.get_all()
    for user in users:
        await send_message(user.user_id, text)