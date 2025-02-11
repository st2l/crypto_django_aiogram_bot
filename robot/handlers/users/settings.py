from robot.models import TelegramUser
from aiogram import types

from loader import dp
from get_bot_info import get_bot_text
from robot.keyboards.default import get_language_keyboard

@dp.callback_query_handler(lambda call: call.data.startswith('settings'), state='*')
async def settings(call: types.CallbackQuery):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    text = "🇬🇧 Choose your language\n🇷🇺 Выберите ваш язык"
    
    await call.answer('')
    await call.message.edit_text(
        text=text,
        reply_markup=await get_language_keyboard(),
        parse_mode='Markdown'
    ) 