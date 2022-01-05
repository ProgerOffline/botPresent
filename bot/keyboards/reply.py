#-*- coding: utf-8 -*-

from logzero import logger
from aiogram import types


def authorization(in_base):
    """
    Возвращает одну кнопку входа, если пользователь есть в базе
    То текст будет "Войти", если нет в базе тогда "Регистрация"
    agrs:
        in_base - Наличие пользователя в базе
    """
    logger.info("Get authorization keyboard")

    if in_base:     
        return types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=1,
        ).add(
            types.KeyboardButton(
                text="Войти",
                request_contact=True,
            ),
        )
    else:
        return types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=1,
        ).add(
            types.KeyboardButton(
                text="Регистрация",
                request_contact=True,
            ),
        )
    

def main_menu():
    logger.info("Get main_menu keyboard")

    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).row(
        types.KeyboardButton(text="Мой Баланс"),
        types.KeyboardButton(text="Пополнить баланс"),
    ).row(
        types.KeyboardButton(text="Реферальная ссылка"),
        types.KeyboardButton(text="Кошелек для вывода"),
    ).row(
        types.KeyboardButton(text="Мои инвестиции"),
        types.KeyboardButton(text="Инвестиционный продукт"),
    ).row(
        types.KeyboardButton(text="Вывод"),
        types.KeyboardButton(text="Профиль"),
    ).row(
        types.KeyboardButton(text="Презентация"),
        types.KeyboardButton(text="Техническая поддержка"),
    ).row(
        types.KeyboardButton(text="Выход"),
    )


def fill_ballance():
    logger.info("Get fill_balance keyboard")

    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).row(
        types.KeyboardButton(text="Сбербанк"),
        types.KeyboardButton(text="Тинькофф"),
    ).row(
        types.KeyboardButton(text="Назад"),
    )


def check_bill():
    logger.info("Get check_bill keyboard")

    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).add(
        types.KeyboardButton(text="Я оплатил"),
        types.KeyboardButton(text="Назад"),
    )


def back_to_menu():
    logger.info("Get back_to_menu keyboard")

    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).add(
        types.KeyboardButton(text="Назад"),
    )


def confirm_purchase():
    logger.info("Get confirm_purchase keyboard")

    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).add(
        types.KeyboardButton(text="Подтвердить покупку"),
        types.KeyboardButton(text="Назад"),
    )


def quest_type():
    logger.info("Get quest_type keyboard")

    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).row(
        types.KeyboardButton(text="Начисление дивидендов"),
        types.KeyboardButton(text="Пополнение баланса"),
    ).row(
        types.KeyboardButton(text="Вывод средств"),
        types.KeyboardButton(text="Другой вопрос")
    ).row(
        types.KeyboardButton(text="Назад")
    )


def exit_corres():
    logger.info("Get exit_corres keyboard")

    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).add(
        types.KeyboardButton(text="Завершить чат"),
    )