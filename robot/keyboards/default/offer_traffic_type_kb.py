import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from robot.models import Offer


async def get_offer_traffic_type_keayboard():

    categories = await sync_to_async(
        Offer.objects.values('traffic_type').distinct, thread_sensitive=True
    )()

    keyboard = InlineKeyboardMarkup()

    async for cat in categories:
        print(cat['traffic_type'], type(cat))
        keyboard.add(InlineKeyboardButton(
            text=cat['traffic_type'], callback_data=f'traffic_type_offer_chosen:{cat["traffic_type"]}'))

    return keyboard
