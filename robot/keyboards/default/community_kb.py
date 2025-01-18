from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from robot.models import CommunityButton
from asgiref.sync import sync_to_async


async def get_community_kb():
    keyboard = InlineKeyboardMarkup()
    buttons = await sync_to_async(
        CommunityButton.objects.all,
        thread_sensitive=True
    )()

    async for button in buttons:
        keyboard.add(
            InlineKeyboardButton(
                text=button.name,
                url=button.url,
            )
        )

    return keyboard
