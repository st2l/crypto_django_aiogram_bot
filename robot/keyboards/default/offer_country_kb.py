import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from robot.models import Offer


async def get_offer_geo_keayboard():

    categories = await sync_to_async(
        Offer.objects.values('geo').distinct, thread_sensitive=True
    )()

    keyboard = InlineKeyboardMarkup()

    async for cat in categories:
        keyboard.add(InlineKeyboardButton(
            text=cat['geo'], callback_data=f'geo_offer_chosen:{cat["geo"]}'))

    return keyboard
