import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from robot.models import Categories


async def get_offer_type_keayboard():

    categories = await sync_to_async(
        Categories.objects.all, thread_sensitive=True
    )()

    keyboard = InlineKeyboardMarkup()

    async for cat in categories:
        keyboard.add(InlineKeyboardButton(
            text=cat.name, callback_data=f'category_offer_chosen:{cat.code}')
        )
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="BACK 🔙", callback_data="main_menu")])

    return keyboard
