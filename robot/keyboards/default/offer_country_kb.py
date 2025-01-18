import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from robot.models import Geos


async def get_offer_geo_keayboard():

    geo_s = await sync_to_async(
        Geos.objects.all, thread_sensitive=True
    )()

    keyboard = InlineKeyboardMarkup()

    async for geo in geo_s:
        keyboard.add(InlineKeyboardButton(
            text=geo.name, callback_data=f'geo_offer_chosen:{geo.code}'))

    return keyboard