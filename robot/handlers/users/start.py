import logging

from asgiref.sync import sync_to_async
from robot.models import TelegramUser

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from get_bot_info import get_bot_text


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=message.from_user.id)
    user = await sync_to_async(telegram_user.get_user)()
    
    text = await get_bot_text('start')
    
    if not text:
        logging.error('Bot text not found')
        return
    
    await message.answer(
        text=text,
    )
