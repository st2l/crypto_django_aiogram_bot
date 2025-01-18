import logging

from robot.models import TelegramUser

from aiogram import types
from asgiref.sync import sync_to_async

from loader import dp
from get_bot_info import get_bot_text
from robot.keyboards.default import get_main_menu_kb
from robot.models import Offer
from collections import Counter


@dp.callback_query_handler(lambda call: call.data.startswith('statistics'))
async def statistics(call: types.CallbackQuery):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    text = await get_bot_text(f'statistics {telegram_user.lang}')
    offers = await sync_to_async(
        Offer.objects.all, thread_sensitive=True
    )()
    offer_counts = dict(Counter([offer.category async for offer in offers]))
    logging.info(offer_counts)
    
    if telegram_user.lang == 'ru':
        text += f'\nВсего офферов: {len(offers)}'
    else:
        text += f'\nTotal offers: {len(offers)}'
    
    for key, val in offer_counts.items():
        text += f'\n{key}: {val}'

    await call.answer('')
    await call.message.answer(
        text=text,
    )
