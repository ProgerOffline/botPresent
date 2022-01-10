#-*- coding: utf-8 -*-

import asyncio

from database import create_db
from logzero import logger

from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewaries.update_logger import UpdateLoggerMiddleware

from data import config
import handlers


bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp):
    await create_db()

    dp.middleware.setup(UpdateLoggerMiddleware())
    handlers.setup(dp, bot)


if __name__ == "__main__":
    logger.info("Starting bot polling...")
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
