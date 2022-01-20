#-*- coding: utf-8 -*-

import os


async def get_picture():
    try:
        path = os.getcwd() + "/precentPicture"
        picture = open(path, "rb")
    except FileNotFoundError:
        return False

    return picture