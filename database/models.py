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
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()
    await db.gino.create_all()


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    phone = Column(BigInteger)
    query: sql.Select


class DBCommands:
    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user
    
    async def add_new_user(self, contact) -> User: 
        old_user = await self.get_user(contact.user_id)
        
        if old_user:
            return old_user
        
        logger.info(f"Add new user: {contact.user_id}, {contact.phone_number}")
        new_user = User()
        new_user.user_id = contact.user_id
        new_user.phone = contact.phone_number

        await new_user.create()
        return new_user
    
    async def get_all_users(self):
        users = await User.query.gino.all()
        return users