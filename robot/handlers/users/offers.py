import logging

from robot.models import TelegramUser
from aiogram import types

from loader import dp
from get_bot_info import get_bot_text
from robot.keyboards.default import get_offer_type_keayboard, get_offer_geo_keayboard, get_offer_traffic_type_keayboard, get_back_kb
from robot.utils.db_api import get_offers_by_data

# FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ChooseOffer(StatesGroup):
    category = State()
    geo = State()
    traffic_type = State()


@dp.callback_query_handler(lambda call: call.data.startswith('offers'), state='*')
async def language_change(call: types.CallbackQuery):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    # state FSM to category
    await ChooseOffer.category.set()

    await call.answer('')
    await call.message.edit_text(
        text=await get_bot_text(f'offers clicked {telegram_user.lang}'),
        reply_markup=await get_offer_type_keayboard(),
        parse_mode='Markdown'
    )


@dp.callback_query_handler(lambda call: call.data.startswith('category_offer_chosen'), state=ChooseOffer.category)
async def category_offer_chosen(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    chosen_category = call.data.split(':')[-1]
    logging.info(f'Chosen category: {chosen_category}')

    if chosen_category != 'continue':
        # update state in FSM
        async with state.proxy() as data:
            arr = data.get('category', [])
            arr.append(chosen_category)
            data['category'] = arr
            
            # Формируем текст с выбранными категориями
            categories_text = await get_bot_text(f'offers category chosen {telegram_user.lang}') + \
                ("\nВыбранные категории:\n" if telegram_user.lang == 'ru' else "\nSelected categories:\n")
            for category in arr:
                categories_text += f"• {category}\n"
            
        await call.answer('')
        await call.message.edit_text(
            text=categories_text,
            reply_markup=await get_offer_type_keayboard(),
            parse_mode='Markdown'
        )
    else:
        await ChooseOffer.geo.set()

        await call.answer('')
        await call.message.edit_text(
            text=await get_bot_text(f'offers category chosen {telegram_user.lang}'),
            reply_markup=await get_offer_geo_keayboard(),
            parse_mode='Markdown'
        )


@dp.callback_query_handler(lambda call: call.data.startswith('geo_offer_chosen'), state=ChooseOffer.geo)
async def geo_offer_chosen(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    chosen_geo = call.data.split(':')[-1]
    logging.info(f'Chosen geo: {chosen_geo}')

    if chosen_geo != 'continue':
        async with state.proxy() as data:
            arr = data.get('geo', [])
            arr.append(chosen_geo)
            data['geo'] = arr
            
            # Формируем текст с выбранными гео
            geo_text = await get_bot_text(f'offers geo chosen {telegram_user.lang}') + \
                ("\nВыбранные страны:\n" if telegram_user.lang == 'ru' else "\nSelected countries:\n")  
            for geo in arr:
                geo_text += f"• {geo}\n"
        
        await call.answer('')
        await call.message.edit_text(
            text=geo_text,
            reply_markup=await get_offer_geo_keayboard(),
            parse_mode='Markdown'
        )
    else:
        await ChooseOffer.traffic_type.set()
        await call.answer('')
        await call.message.edit_text(
            text=await get_bot_text(f'offers geo chosen {telegram_user.lang}'),
            reply_markup=await get_offer_traffic_type_keayboard(),
            parse_mode='Markdown'
        )


@dp.callback_query_handler(lambda call: call.data.startswith('traffic_type_offer_chosen'), state=ChooseOffer.traffic_type)
async def traffic_type_offer_chosen(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    chosen_traffic_type = call.data.split(':')[-1]
    logging.info(f'Chosen traffic_type: {chosen_traffic_type}')

    if chosen_traffic_type != 'continue':
        async with state.proxy() as data:
            arr = data.get('traffic_type', [])
            arr.append(chosen_traffic_type)
            data['traffic_type'] = arr

            # Формируем текст с выбранными типами трафика
            traffic_text = await get_bot_text(f'offers geo chosen {telegram_user.lang}') + \
                ("\nВыбранные типы трафика:\n" if telegram_user.lang == 'ru' else "\nSelected traffic types:\n")
            for traffic_type in arr:
                traffic_text += f"• {traffic_type}\n"

            await call.answer('')
            await call.message.edit_text(
                text=traffic_text,
                reply_markup=await get_offer_traffic_type_keayboard(),
                parse_mode='Markdown'
            )
    else:
        # update state in FSM
        # change it to traffic_type
        async with state.proxy() as data:

            logging.info(f'Offer data: {data}')

            offer_by_data = await get_offers_by_data(data)

            if not offer_by_data:
                if telegram_user.lang == 'ru':
                    text = "По вашему запросу ничего не найдено"
                else:
                    text = "Nothing found by your request"

                await call.answer('')
                await call.message.edit_text(
                    text=text,
                    reply_markup=await get_back_kb(),
                )
                await state.finish()
                return

            for offer in offer_by_data:

                if telegram_user.lang == 'ru':
                    text = ""

                    text += f'Название оффера: {offer.name}\n' + \
                        f'Гео: {offer.geo}\n' + \
                            f'Тип трафика: {offer.traffic_type}\n'

                    kb = types.InlineKeyboardMarkup(inline_keyboard=[
                        [types.InlineKeyboardButton(
                            text='Перейти к офферу', url=offer.offer_link)]
                    ])

                    await call.answer('')
                    await call.bot.send_message(
                        chat_id=call.from_user.id,
                        text=text,
                        reply_markup=kb,
                        parse_mode='Markdown'
                    )
                else:
                    text = ""

                    text += f'Offer name: {offer.name}\n' + \
                        f'Geo: {offer.geo}\n' + \
                            f'Traffic type: {offer.traffic_type}\n'

                    kb = types.InlineKeyboardMarkup(inline_keyboard=[
                        [types.InlineKeyboardButton(
                            text='Go to offer', url=offer.offer_link)]
                    ])

                    await call.answer('')
                    await call.bot.send_message(
                        chat_id=call.from_user.id,
                        text=text,
                        reply_markup=kb,
                        parse_mode='Markdown'

                    )

        await state.finish()
