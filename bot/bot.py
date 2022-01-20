# -*- coding: utf-8 -*-

import asyncio
import handlers

from logzero import logger
from data import config
from database import create_db
from utils.time_functions import count_users_invest

from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewaries.update_logger import UpdateLoggerMiddleware

from apscheduler.schedulers.asyncio import AsyncIOScheduler


bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

async def on_startup(dp):
    await create_db()

    scheduler.start()
    scheduler.add_job(count_users_invest, "interval", seconds=10, args=(bot, ))
    dp.middleware.setup(UpdateLoggerMiddleware())
    handlers.setup(dp, bot)


if __name__ == "__main__":
    try:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
