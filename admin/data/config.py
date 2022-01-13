#-*- coding: utf-8 -*-

from environs import Env

env = Env()
env.read_env()

DB_PASS = env.str("DB_PASS")
DB_USER = env.str("DB_USER")
DB_HOST = env.str("DB_HOST")
BOT_TOKEN = env.str("BOT_TOKEN")