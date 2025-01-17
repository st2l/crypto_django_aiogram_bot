import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from robot.models import Offer


async def get_offer_type_keayboard():

    categories = await sync_to_async(
        Offer.objects.values('category').distinct, thread_sensitive=True
    )()

    keyboard = InlineKeyboardMarkup()

    async for cat in categories:
        print(cat['category'], type(cat))
        keyboard.add(InlineKeyboardButton(
            text=cat['category'], callback_data=f'category_offer_chosen:{cat["category"]}'))

    return keyboard
