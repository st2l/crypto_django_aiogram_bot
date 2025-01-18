import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from robot.models import TrafficTypes


async def get_offer_traffic_type_keayboard():

    traffic_types = await sync_to_async(
        TrafficTypes.objects.all, thread_sensitive=True
    )()

    keyboard = InlineKeyboardMarkup()

    async for traffic_type in traffic_types:
        keyboard.add(InlineKeyboardButton(
            text=traffic_type.name,
            callback_data=f'traffic_type_offer_chosen:{traffic_type.name}')
        )

    return keyboard
