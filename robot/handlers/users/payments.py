from robot.models import TelegramUser

from aiogram import types

from loader import dp
from get_bot_info import get_bot_text
from robot.keyboards.default import get_main_menu_kb


@dp.callback_query_handler(lambda call: call.data.startswith('payments'))
async def payments(call: types.CallbackQuery):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    await call.answer('')
    await call.message.answer(
        text=await get_bot_text(f'payments {telegram_user.lang}'),
    )
