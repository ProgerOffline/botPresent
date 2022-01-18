#-*- coding: utf-8 -*-

from data.config import DB_HOST, DB_USER, DB_PASS
from database.models import db

from . import models
from . import referers_api
from . import support_api
from . import users_api
from . import outs_api

from loader import app


@app.before_serving
async def create_db():
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/gino")