#-*- coding: utf-8 -*-

from data.config import DB_HOST, DB_USER, DB_PASS
from database.models import db, InvestProduct, Settings


async def create_db():
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/gino")
    # await db.gino.drop_all()
    # await db.gino.create_all()

    await fill_constants_data()
    await fill_invest_product_data()


async def fill_invest_product_data():
    new_proudct = InvestProduct()
    new_proudct.precent = 5
    await new_proudct.create()


async def fill_constants_data():
    new_constant = Settings()
    new_constant.precent = 5.0
    new_constant.cber_bank = 0
    new_constant.tinkoff_bank = 0
    new_constant.fio_cber = " "
    new_constant.fio_tinkoff = " "
    new_constant.wallet_pm = ""
    new_constant.pm_account = 0
    new_constant.pm_passwd = ""
    new_constant.support_chat_id = 0
    await new_constant.create()
