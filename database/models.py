#-*- coding: utf-8 -*-

from aiogram import types
from logzero import logger
from data.config import DB_HOST, DB_USER, DB_PASS
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import sql
from sqlalchemy import (Column, Integer, BigInteger, String,
                       Sequence, TIMESTAMP, Boolean, JSON)


db = Gino()


async def create_db():
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/gino")
    await db.gino.drop_all()
    await db.gino.create_all()


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String(length=50))
    phone = Column(BigInteger)
    query: sql.Select