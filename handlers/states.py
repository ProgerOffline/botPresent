#-*- coding: utf-8 -*-

from re import M
import keyboards

from data.config import SUPPORT_CHANNEL_ID 
from aiogram import types
from keyboards import reply
from statesgroup import InvestProduct, Payment, Support, Wallet
from aiogram.dispatcher import FSMContext
from database import users_api, support_api


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

        await state.update_data(amount=amount)

        msg = "📌 <b>ПОРЯДОК ДЕЙСТВИЙ ДЛЯ СОВЕРШЕНИЯ ОБМЕНА:</b>\n\n" + \
            "1️⃣ Перейдите на сайт <a href=''>Сбербанк онлайн</a>" + \
                " / <a href=''>Тинькофф онлайн</a>" + \
                " и войдите в кабинет пользователя.\n" + \
            "2️⃣ Совершите платеж на сумму <b>500.00 RUB</b>, " + \
                "с точностью до 1 копейки.\n" + \
            "3️⃣ Номер карты для перевода  - 4800123412341234.\n" + \
            "4️⃣ Ф.И.О. получателя -  Б ЕВГЕНИЙ ВЛАДИМИРОВИЧ.\n" + \
            "5️⃣ Комментарий к  переводу -  Мой телефон +79112223333.\n\n" + \
            "❗️ Правильно указывайте «комментарии к платежу / сообщение " + \
                "получателю», а именно: <b>«Мой телефон +79112223333»</b>. " + \
                "В противном случае платеж не будет идентифицирован.\n\n" + \
            "✅ После оплаты кликните по кнопке <b>«Я оплатил»</b>, чтобы " + \
                "мы получили уведомление и проверили поступление средств."
        await message.answer(
            text=msg,
            reply_markup=keyboards.reply.check_bill(),
        )
        
        await Payment.payment_check.set()
    
    @dp.message_handler(state=Wallet.set_wallet)
    async def set_wallet(message: types.Message, state: FSMContext):
        if message.text[0] != "U" and message.text[0] != "u":
            msg = "⚠️ Ошибка: Недопустимый формат кошелька." + \
                    "Проверьте правильность написания" 
            await message.answer(
                text=msg,
            )
            await state.finish()
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
                text="⚠️ Ошибка: Минимальная сумма инвестиции кратное от $1000",
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
            reply_markup=keyboards.reply.back_to_menu(),
        )

        msg = f"💬 Новый вопрос от <code>{message.from_user.username}</code>\n" + \
            f"ℹ️ Тип вопроса: {corres.quest_type}\n\n" + \
            f"Полный вопрос: {corres.quest_full}"
        msg = await bot.send_message(
            chat_id=SUPPORT_CHANNEL_ID,
            text=msg,
            reply_markup=keyboards.inline.answer(corres.id),
        )

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

            await bot.send_message(
                chat_id=companion_id,
                text=f"<code>{message.from_user.username}</code> завершил чат",
                reply_markup=keyboards.reply.main_menu(),
            )

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Вы успешно завершили чат",
                reply_markup=keyboards.reply.main_menu(),
            )

            await bot.edit_message_text(
                chat_id=SUPPORT_CHANNEL_ID,
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