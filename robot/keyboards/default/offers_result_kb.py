from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from robot.models import Offer


async def get_offers_result_kb(offer_data: list[Offer], page: int = 0):
    kb = InlineKeyboardMarkup()

    if len(offer_data) > 5:
        kb.add(InlineKeyboardButton(text="◀️", callback_data="offer_prev_page"))

    for offer in offer_data[page*5:(page+1)*5]:
        kb.add(InlineKeyboardButton(text=offer.name,
               callback_data=f"offer_get_id:{offer.id}"))
        
    if len(offer_data) > 5:
        kb.add(InlineKeyboardButton(text="➡️", callback_data="offer_next_page"))

    kb.add(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_offers"))
    return kb
