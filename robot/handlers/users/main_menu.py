from robot.models import TelegramUser

from aiogram import types

from loader import dp
from get_bot_info import get_bot_text 
from robot.keyboards.default import get_main_menu_kb

# FSM
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda call: call.data.startswith('main_menu'), state='*')
async def main_menu(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    await state.finish()

    await call.answer('')
    await call.message.answer(
        text=await get_bot_text(f'main menu {telegram_user.lang}'),
        reply_markup=await get_main_menu_kb(),
        parse_mode='Markdown'
    )
