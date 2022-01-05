#-*- coding: utf-8 -*-

from aiogram.dispatcher.filters.state import State, StatesGroup

class Payment(StatesGroup):
    payment_amount = State()
    payment_check = State()


class Wallet(StatesGroup):
    set_wallet = State()


class InvestProduct(StatesGroup):
    set_invest_amount = State()
    confirm_purchase = State()


class Support(StatesGroup):
    quest_full = State()
    corres = State()