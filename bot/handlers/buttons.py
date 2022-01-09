#-*- coding: utf-8 -*-

from aiogram import types
from database import users_api
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from statesgroup import Payment, Support, Wallet, InvestProduct

import keyboards


def setup(dp):
    @dp.message_handler(filters.Text(contains="Назад"))
    async def back(message: types.Message):
        await message.answer(
            text="🗃 Выберите раздел.",
            reply_markup=keyboards.reply.main_menu(),
        )

    @dp.message_handler(filters.Text(contains="Мой Баланс"))
    async def ballance(message: types.Message):
        user = await users_api.get_user(message.from_user.id)
        ballance = float('{:.3f}'.format(user.ballance))
        await message.answer(
            text=f"💰 Текущий баланс: {ballance} RUB",
        )

    @dp.message_handler(filters.Text(contains="Пополнить баланс"))
    async def fill_ballance(message: types.Message):
        await message.answer(
            text="⚖️ Выберите метод пополнения",
            reply_markup=keyboards.reply.fill_ballance(),
        )

    @dp.message_handler(filters.Text(contains="Сбербанк"))
    @dp.message_handler(filters.Text(contains="Тинькофф"))
    async def payment_type(message: types.Message):
        await Payment.payment_amount.set()
        await message.answer(
            text="💵 Введите сумму в RUB",
        )

    @dp.message_handler(
        filters.Text(contains="Я оплатил"), state=Payment.payment_check)
    async def check_bill(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            amount = data['amount']

        user = await users_api.get_user(message.from_user.id)
        amount = user.ballance + amount
        await users_api.set_ballance(
            user_id=message.from_user.id,
            amount=amount,
        )

        await message.answer(
            text=f"⏳ Ожидайте поступление денежных средств на Ваш " + \
                "баланс в течение 24 часов.",
        )
        await state.finish()

    @dp.message_handler(filters.Text(contains="Реферальная ссылка"))
    async def ref_link(message: types.Message):
        user = await users_api.get_user(message.from_user.id)

        if user.buyed:
            msg = "🔗 Скопируйте и отправьте ссылку новому партнеру: " + \
                f"https://t.me/tg4bot_bot?start=referer_{user.id}"
        else:
            msg = "⚠️ Для получения возможность получать доход от рефералов " + \
                "Вам необходимо приобрести инвестиционный продукт."

        await message.answer(
            text=msg,
        )

    @dp.message_handler(filters.Text(contains="Мои инвестиции"))
    async def my_investments(message: types.Message):
        user = await users_api.get_user(message.from_user.id)

        if user.invest_amount <= 0:
            msg = "💵 Инвестиций не найдено"
        else:
            msg = f"💵 Инвестировано {user.invest_amount} RUB"

        await message.answer(
            text=msg,
        )

    @dp.message_handler(filters.Text(contains="Кошелек для вывода"))
    async def wallet_out(message: types.Message):
        user = await users_api.get_user(message.from_user.id)
        msg = "💲  Введите ваш долларовый кошелек платежной системы " + \
            "Perfect Money.\nПример кошелька: U1234567\n" + \
            "📌 Как зарегистрировать кошелек Perfect Money" + \
            " можете прочитать в данной статье htts://"

        await Wallet.set_wallet.set()
        await message.answer(
            text=msg,
        )

    @dp.message_handler(filters.Text(contains="Инвестиционный продукт"))
    async def invest_product(message: types.Message):
        msg = "ЕЖЕДНЕВНАЯ ДОХОДНОСТЬ 5-10%\n\n" + \
            "▪️ Депозит от 1000 RUB.\n" + \
            "▪️Ввод Сбербанк / Тинькофф  и вывод Perfect Money.\n" + \
            "▪️Вывод дивидендов каждый день.\n" + \
            "▪️Срок контракта: не ограничен.\n\n" + \
            "💵 Введите сумму, которую хотите инвестировать в RUB"
    
        await InvestProduct.set_invest_amount.set()
        await message.answer(
            text=msg,
            reply_markup=keyboards.reply.back_to_menu(),
        )
    
    @dp.message_handler(
        filters.Text(contains="Подтвердить покупку"), 
        state=InvestProduct.confirm_purchase)
    async def confirm_purchase(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            amount = data['amount']

        user = await users_api.get_user(message.from_user.id)

        ballance = user.ballance - amount
        print(ballance)
        await users_api.set_ballance(message.from_user.id, ballance)

        invest_amount = user.invest_amount + amount
        await users_api.set_invest_amount(message.from_user.id, invest_amount)

        msg = "✅ Инвестиционный продукт успешно оплачен. " + \
                "Каждые 24 часа вам будут начисляться дивиденды."
        await state.finish()
        await message.answer(
            text=msg,
        )

    @dp.message_handler(
        filters.Text(contains="Назад"), 
        state=InvestProduct.confirm_purchase)
    async def back_to_menu(message: types.Message, state: FSMContext):
        await state.finish()
        await message.answer(
            text="🗃 Выберите раздел.",
            reply_markup=keyboards.reply.main_menu(),
        )
    
    @dp.message_handler(filters.Text(contains="Выход"))
    async def logout(message: types.Message):
        await message.answer(
            text="🙏🏻 Спасибо, что Вы с нами! Ждем Вас снова.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    
    @dp.message_handler(filters.Text(contains="Презентация"))
    async def presentation(message: types.Message):
        await message.answer(
            text="🔗Ссылка на презентацию: https://",
        )
    
    @dp.message_handler(filters.Text(contains="Техническая поддержка"))
    async def support(message: types.Message):
        await message.answer(
            text="Выберите тип вашего вопроса",
            reply_markup=keyboards.reply.quest_type(),
        )
    
    @dp.message_handler(filters.Text(contains="Начисление дивидендов"))
    @dp.message_handler(filters.Text(contains="Пополнение баланса"))
    @dp.message_handler(filters.Text(contains="Вывод средств"))
    @dp.message_handler(filters.Text(contains="Другой вопрос"))
    async def quest_type(message : types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['quest_type'] = message.text
        
        await Support.quest_full.set()
        await message.answer(
            text="Пожалуйста, введите свой вопрос",
        )
        
    
    @dp.message_handler(filters.Text(contains="Профиль"))
    async def profile(message: types.Message):
        user = await users_api.get_user(message.from_user.id)

        wallet = user.wallet if user.wallet != "" else "⚠️ Привяжите кошелек"
        referer = user.referer if user.referer != 0 else "У вас нет пригласителя"
        month = user.reg_date.month
        month = month if month >= 10 else f"0{month}"
        day = user.reg_date.day
        day = day if day >= 10 else f"0{day}"
        
        msg = f"Имя: {message.from_user.first_name}\n" + \
            f"Фамилия: {message.from_user.last_name}\n" + \
            f"Ваш ID: {user.id}\n" + \
            f"ID пригласителя: {referer}\n" + \
            f"Кошелек PM: {wallet}\n" + \
            f"Дата регистрации: {day}.{month}.{user.reg_date.year}"
        
        await message.answer(
            text=msg,
        )
    