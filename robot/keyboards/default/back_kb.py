from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_button = InlineKeyboardButton(text="BACK 🔙", callback_data="main_menu")

async def get_back_kb():
    return InlineKeyboardMarkup().add(back_button)