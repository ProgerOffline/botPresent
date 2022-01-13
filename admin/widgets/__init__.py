#-*- coding: utf-8 -*-

import aiohttp
import requests
from data.config import BOT_TOKEN


async def send_message(user_id, text):
    url = "https://api.telegram.org/bot" + BOT_TOKEN
    url += "/sendMessage"
    data = {
        "chat_id" : user_id,
        "text" : text,
    }
    async with aiohttp.ClientSession() as session:
        await session.get(url, params=data)

