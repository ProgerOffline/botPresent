#-*- coding: utf-8 -*-

from logzero import logger

from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

import handlers

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

handlers.setup(dp)

if __name__ == "__main__":
    logger.info("Starting bot polling...")
    executor.start_polling(dp)