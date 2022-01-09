#-*- coding: utf-8 -*-

from data.config import DB_HOST, DB_USER, DB_PASS
from database.models import db


async def create_db():
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/gino")