from aiogram import types


def setup(dp) -> None:
    @dp.message_handler()
    async def echo(message: types.Message):
        await message.answer(
            text=message.text,
        )