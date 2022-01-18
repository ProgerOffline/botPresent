#-*- coding: utf-8 -*-

from loader import app
from database import *
from api import *
from pages import *
from data.config import FLASK_HOST


if __name__ == "__main__":
    app.run(host=FLASK_HOST)
