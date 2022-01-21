#-*- coding: utf-8 -*-

import keyboards

from aiogram import types
from statesgroup import InvestProduct, Payment, Support, Wallet, OutMoney
from aiogram.dispatcher import FSMContext
from database import users_api, support_api, payments_api, settings_api
from aiogram.utils.exceptions import ChatNotFound


def setup(dp, bot):
    @dp.message_handler(state=Payment.payment_amount)
    async def payment_amount(message: types.Message, state: FSMContext):
        if "Назад" in message.text:
            await state.finish()
            await message.answer(
                text="🗃 Выберите раздел.",
                reply_markup=keyboards.reply.main_menu(),
            )
            return

        try:
            amount = float(message.text)
        except ValueError:
            await message.answer(
                text="⚠️ Ошибка: Минимальная сумма пополнения 500.00 RUB"
            )   
            return

        user = await users_api.get_user(message.from_user.id)
        constants = await settings_api.get_constants()
        data = await state.get_data()

        site = "<a href='https://sber.ru/bank/'>Сбербанк</a>" \
            if data['bank'] == "Сбербанк" \
            else  "<a href='https://www.tinkoff.ru/'>Тинькофф</a>"
        card = constants.cber_bank \
            if "sber" in site \
            else constants.tinkoff_bank
        fio = constants.fio_cber \
            if "sber" in site \
            else constants.fio_tinkoff
            
        msg = "📌 <b>ПОРЯДОК ДЕЙСТВИЙ ДЛЯ СОВЕРШЕНИЯ ОБМЕНА:</b>\n\n" + \
            f"1️⃣ Перейдите на сайт {site}" + \
                " и войдите в кабинет пользователя.\n" + \
            f"2️⃣ Совершите платеж на сумму <b>{amount} RUB</b>, " + \
                "с точностью до 1 копейки.\n" + \
            f"3️⃣ Номер карты для перевода  - <code>{card}</code>.\n" + \
            f"4️⃣ Ф.И.О. получателя -  {fio}\n" + \
            f"5️⃣ Комментарий к  переводу -  Мой телефон {user.phone}.\n\n" + \
            "❗️ Правильно указывайте «комментарии к платежу / сообщение " + \
            f"получателю», а именно: <b>«Мой телефон {user.phone}»</b>. " + \
            "В противном случае платеж не будет идентифицирован.\n\n" + \
            "✅ После оплаты кликните по кнопке <b>«Я оплатил»</b>, чтобы " + \
            "мы получили уведомление и проверили поступление средств."

        await message.answer(
            text=msg,
            reply_markup=keyboards.reply.check_bill(),
            disable_web_page_preview=True,
        )
        
        payment = await payments_api.add_payment(
            user_id=message.from_user.id,
            bank=data['bank'],
            amount=amount,
        )

        await state.update_data(amount=amount)
        await state.update_data(payment_id=payment.id)
        await Payment.payment_check.set()
    
    @dp.message_handler(state=Wallet.set_wallet)
    async def set_wallet(message: types.Message, state: FSMContext):
        if message.text == "Назад":
            await state.finish()
            await message.answer(
                text="🗃 Выберите раздел.",
                reply_markup=keyboards.reply.main_menu(),
            )
            return

        if message.text[0] != "U" and message.text[0] != "u":
            await state.finish()
            msg = "⚠️ Ошибка: Недопустимый формат кошелька. " + \
                    "Проверьте правильность написания"
            await message.answer(
                text=msg,
            )
            return
        
        await users_api.set_wallet(
            user_id=message.from_user.id,
            wallet=message.text,
        )

        await state.finish()
        await message.answer(
            text="✅ Кошелек для вывода успешно добавлен.",
        )
    
    @dp.message_handler(state=InvestProduct.set_invest_amount)
    async def set_invest_amount(message: types.Message, state: FSMContext):
        if "Назад" in message.text:
            await state.finish()
            await message.answer(
                text="🗃 Выберите раздел.",
                reply_markup=keyboards.reply.main_menu(),
            )
            await state.finish()
            return

        try:
            amount = float(message.text)
        except ValueError:
            await message.answer(
                text="⚠️ Ошибка: сумма должна состоять только из цифр",
            )
            return
        
        if amount < 1000:
            await message.answer(
                text="⚠️ Ошибка: Минимальная сумма инвестиции от 1000 RUB",
            )
            return
        
        user = await users_api.get_user(message.from_user.id)
        if user.ballance < amount:
            await message.answer(
                text="⚠️ Ошибка: Суммы на балансе не достаточно",
            )
            return
        
        async with state.proxy() as data:
            data['amount'] = amount

        await InvestProduct.confirm_purchase.set()
        await message.answer(
            text="Вы подтверждаете покупку?",
            reply_markup=keyboards.reply.confirm_purchase(),
        )

    @dp.message_handler(state=Support.quest_full)
    async def quest_full(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            quest_type = data['quest_type']
        
        corres = await support_api.create_corres(
            user_id=message.from_user.id,
            quest_type=quest_type,
            quest_full=message.text,
            msg_id=message
        )

        await Support.corres.set()
        async with state.proxy() as data:
            data['corres_id'] = corres.id
        
        msg = f"🗃 Номер вашего обращения — {corres.id}. " + \
                "Оператор уже подключается к вам."
        await message.answer(
            text=msg,
            reply_markup=keyboards.reply.exit_corres(),
        )

        constants = await settings_api.get_constants()
        msg = f"💬 Новый вопрос от <code>{message.from_user.username}</code>\n" + \
            f"ℹ️ Тип вопроса: {corres.quest_type}\n\n" + \
            f"Полный вопрос: {corres.quest_full}"

        try:
            msg = await bot.send_message(
                chat_id=constants.support_chat_id,
                text=msg,
                reply_markup=keyboards.inline.answer(corres.id),
            )
        except ChatNotFound:
            await state.finish()
            await message.answer(
                text="⚠️ Ошибка: id чата тех поддержки не существует",
                reply_markup=keyboards.reply.main_menu(),
            )
            return

        await support_api.set_msg_id(corres.id, msg.message_id)
        
    @dp.message_handler(state=Support.corres)
    async def corres(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            corres_id = data['corres_id']

        corres = await support_api.get_corres(corres_id)

        if message.text == "Завершить чат":
            if message.from_user.id == corres.user_id:
                companion_id = corres.support_id
            else:
                companion_id = corres.user_id

            try:
                await bot.send_message(
                    chat_id=companion_id,
                    text=f"<code>{message.from_user.username}</code> завершил чат",
                    reply_markup=keyboards.reply.main_menu(),
                )
            except ChatNotFound:
                pass

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Вы успешно завершили чат",
                reply_markup=keyboards.reply.main_menu(),
            )

            constants = await settings_api.get_constants()
            await bot.edit_message_text(
                chat_id=constants.support_chat_id,
                message_id=corres.msg_id,
                text="ℹ️ Вопрос завершен, или отменен",
            )
            await state.finish()
            await dp.current_state(chat=companion_id, user=companion_id).finish()
            return
            
        if corres.user_id == message.from_user.id:
            await bot.send_message(
                chat_id=corres.support_id,
                text=message.text,
            )
        
        if corres.support_id == message.from_user.id:
            await bot.send_message(
                chat_id=corres.user_id,
                text=message.text,
            )
        
    @dp.message_handler(state=OutMoney.set_amount)
    async def set_amount(message: types.Message, state: FSMContext):
        if message.text == "Назад":
            await state.finish()
            await message.answer(
                text="🗃 Выберите раздел.",
                reply_markup=keyboards.reply.main_menu(),
            )
            return

        user = await users_api.get_user(message.from_user.id)
        
        if ("U" not in user.wallet) or ("U" not in user.wallet):
            await message.answer(
                text="⚠️ Ошибка: Привяжите кошелек Perfect Money",
            )
            await state.finish()
            return

        try:
            amount = int(message.text)
        except ValueError:
            await message.answer(
                text="⚠️ Ошибка: сумма должна состоять только из цифр",
            )
            await state.finish()
            return
        
        if amount < 500:
            await message.answer(
                text="⚠️ Ошибка: Минимальная сумма вывода 500 RUB."
            )
            await state.finish()
            return
        
        if user.ballance < amount:
            await message.answer(
                text="⚠️ Ошибка: На вашем балансе недостаточно средств."
            )
            await state.finish()
            return
        
        await state.update_data(amount=amount)
        await OutMoney.confirm_out.set()
        await message.answer(
            text="❗️ Проверьте данные ❗️\n" + \
                f"Вывод на кошелек PM: {user.wallet}.\n" + \
                f"Сумма вывода: {amount} RUB.\n\n" + \
                "Внимательно проверьте данные перед подтверждением вывода.",
            reply_markup=keyboards.reply.confirm_out(),
        )