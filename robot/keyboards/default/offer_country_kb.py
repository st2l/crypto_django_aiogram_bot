import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from robot.models import Geos


async def get_offer_geo_keayboard(chosen_geo: list = []):

    geo_s = await sync_to_async(
        Geos.objects.all, thread_sensitive=True
    )()

    keyboard = InlineKeyboardMarkup(row_width=3)

    async for geo in geo_s:
        keyboard.add(InlineKeyboardButton(
            text=f"{'✅' if geo.code in chosen_geo else ''} {geo.name}", 
            callback_data=f'geo_offer_chosen:{geo.code}'))
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="BACK 🔙", callback_data="main_menu")])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="Continue ⏭", callback_data="geo_offer_chosen:continue")])


    return keyboard
