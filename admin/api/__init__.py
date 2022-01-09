#-*- coding: utf-8 -*-

from flask_app import app


@app.route("/")
async def index():
    return render_template("index.html")