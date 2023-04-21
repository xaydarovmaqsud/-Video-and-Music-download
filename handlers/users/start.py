from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer('Assalomu alaykum.\nQo\'shiq topish uchun:\n1. Instagram link\n2. Video\n3. Audio\n4. Ovozli habar yuboring')
