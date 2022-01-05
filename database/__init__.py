#-*- coding: utf-8 -*-

from data.config import DB_HOST, DB_USER, DB_PASS
from database.models import db, ReferalProgramLevels, InvestProduct


async def create_db():
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/gino")
    await db.gino.drop_all()
    await db.gino.create_all()

    await fill_ref_program_data()
    await fill_invest_product_data()


async def fill_ref_program_data():
    new_level = ReferalProgramLevels()
    new_level.level = 1
    new_level.precent = 20
    await new_level.create()

    new_level = ReferalProgramLevels()
    new_level.level = 2
    new_level.precent = 10
    await new_level.create()

    new_level = ReferalProgramLevels()
    new_level.level = 3
    new_level.precent = 5
    await new_level.create()


async def fill_invest_product_data():
    new_proudct = InvestProduct()
    new_proudct.precent = 5
    await new_proudct.create()