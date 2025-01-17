from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create inline keyboard buttons
offers_button = InlineKeyboardButton(text="OFFERS", callback_data="offers")
payments_button = InlineKeyboardButton(
    text="PAYMENTS", callback_data="payments")
statistics_button = InlineKeyboardButton(
    text="STATISTICS", callback_data="statistics")
community_button = InlineKeyboardButton(
    text="COMMUNITY", callback_data="community")
settings_button = InlineKeyboardButton(
    text="SETTINGS", callback_data="settings")

# Create inline keyboard markup


async def get_main_menu_kb():
    main_menu_kb = InlineKeyboardMarkup(row_width=1).add(
        offers_button,
        payments_button,
        statistics_button,
        community_button,
        settings_button
    )
    return main_menu_kb
