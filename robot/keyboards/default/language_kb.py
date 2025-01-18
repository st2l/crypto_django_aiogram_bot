from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_language_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="English 🇬🇧", callback_data="change_language:en"),
             InlineKeyboardButton(text="Русский 🇷🇺", callback_data="change_language:ru")],
        ],
        row_width=2
    )

    return keyboard
