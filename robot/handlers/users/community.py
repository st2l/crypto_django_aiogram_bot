import logging

from robot.models import TelegramUser
from aiogram import types

from loader import dp
from get_bot_info import get_bot_text
from robot.keyboards.default import get_community_kb
from robot.utils.db_api import get_offers_by_data

# FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


@dp.callback_query_handler(lambda call: call.data.startswith('community'), state='*')
async def community(call: types.CallbackQuery):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    await call.answer('')
    await call.message.answer(
        text=await get_bot_text(f'community {telegram_user.lang}'),
        reply_markup=await get_community_kb(),
        parse_mode='Markdown'
        
    )