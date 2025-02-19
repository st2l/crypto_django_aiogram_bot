from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from robot.models import Service

async def get_services_result_kb(services: list[Service], page: int = 0):
    kb = InlineKeyboardMarkup()

    if len(services) > 5:
        kb.add(InlineKeyboardButton(text="◀️", callback_data="service_prev_page"))

    for service in services[page*5:(page+1)*5]:
        kb.add(InlineKeyboardButton(text=service.name,
               callback_data=f"service_get_id:{service.id}"))
        
    if len(services) > 5:
        kb.add(InlineKeyboardButton(text="➡️", callback_data="service_next_page"))

    kb.add(InlineKeyboardButton(text="🔙 Back", callback_data="main_menu"))
    return kb 