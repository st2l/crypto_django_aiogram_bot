import logging

from asgiref.sync import sync_to_async
from robot.models import TelegramUser

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from get_bot_info import get_bot_text, get_bot_image
from robot.keyboards.default import get_language_keyboard


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=message.from_user.id)
    user = await sync_to_async(telegram_user.get_user)()

    await message.answer_photo(
        caption=await get_bot_text('start'),
        photo=open(await get_bot_image('start'), 'rb'),
        reply_markup=await get_language_keyboard(),
        parse_mode='Markdown'
        
    )


@dp.callback_query_handler(lambda query: query.data == 'start', state='*')
async def start_callback(message: types.Message):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=message.from_user.id)
    user = await sync_to_async(telegram_user.get_user)()

    await message.answer_photo(
        caption=await get_bot_text('start'),
        photo=open(await get_bot_image('start'), 'rb'),
        reply_markup=await get_language_keyboard(),
        parse_mode='Markdown'
        
    )
