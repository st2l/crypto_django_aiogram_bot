from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async
from robot.models import ServiceCategories

async def get_service_type_keyboard(chosen_category: list = []):
    keyboard = InlineKeyboardMarkup()
    
    service_categories = await sync_to_async(ServiceCategories.objects.all, thread_sensitive=True)()

    async for cat in service_categories:
        keyboard.add(InlineKeyboardButton(
            text=("✅" if cat.code in chosen_category else "") + cat.name, callback_data=f'category_service_chosen:{cat.code}')
        )
    keyboard.row(InlineKeyboardButton(text="Continue", callback_data="category_service_chosen:continue"))
    keyboard.row(InlineKeyboardButton(text="BACK 🔙", callback_data="main_menu"))

    return keyboard
