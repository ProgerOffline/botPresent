#-*- coding: utf-8 -*-

from loader import app
from quart import render_template


@app.route("/")
async def page_index():
    return await render_template("index.html")