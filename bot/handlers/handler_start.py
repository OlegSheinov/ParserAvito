from aiogram import types


async def send_welcome(message: types.Message):
    await message.answer('Введи название города:')
