#-*- coding: utf-8 -*-

import keyboards 
from aiogram import types
from statesgroup import Support
from database import users_api, support_api, referers_api


def setup(dp, bot):
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message, state="*"):
        args = message.get_args()

        if "answer" in args:
            corres_id = int(args.split("_")[1])
            await support_api.set_support_id(corres_id, message.from_user.id)
            corres = await support_api.get_corres(corres_id)
            
            async with state.proxy() as data:
                data['corres_id'] = corres_id

            await Support.corres.set()
            await bot.send_message(
                chat_id=corres.user_id,
                text="Оператор подключается к чату...",
                reply_markup=keyboards.reply.exit_corres(),
            )

            user = await users_api.get_user(corres.user_id)
            msg = f"Вы подключились к чату с <code>{user.username}</code>"
            await message.answer(
                text=msg,
                reply_markup=keyboards.reply.exit_corres(),
            )
        
        elif "referer" in args:
            referer_id = int(args.split("_")[1])
            await referers_api.create_record(
                referer_id=referer_id, 
                user_id=message.from_user.id,
            )

            is_base = bool(await users_api.get_user(message.from_user.id))

            await message.answer(
                text=" 👋 Добро пожаловать в чат бот компании OKO",
                reply_markup=keyboards.reply.authorization(is_base),
            )
            
        else:
            is_base = bool(await users_api.get_user(message.from_user.id))

            await message.answer(
                text=" 👋 Добро пожаловать в чат бот компании OKO",
                reply_markup=keyboards.reply.authorization(is_base),
            )