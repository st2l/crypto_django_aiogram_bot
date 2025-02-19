from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create inline keyboard buttons
offers_button = InlineKeyboardButton(text="OFFERS 👨‍💻", callback_data="offers")
payments_button = InlineKeyboardButton(
    text="SERVICES 💸", callback_data="services")
statistics_button = InlineKeyboardButton(
    text="STATISTICS 📊", callback_data="statistics")
community_button = InlineKeyboardButton(
    text="COMMUNITY 💬", callback_data="community")
settings_button = InlineKeyboardButton(
    text="SETTINGS ⚙️", callback_data="settings")
back_button = InlineKeyboardButton(
    text="BACK 🔙", callback_data="start")

# Create inline keyboard markup


async def get_main_menu_kb():
    main_menu_kb = InlineKeyboardMarkup(row_width=2).add(
        offers_button,
        payments_button,
        statistics_button,
        community_button,
        settings_button
    )
    return main_menu_kb
