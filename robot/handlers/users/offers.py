import logging

from robot.models import TelegramUser
from aiogram import types

from loader import dp
from get_bot_info import get_bot_text
from robot.keyboards.default import get_offer_type_keayboard, get_offer_geo_keayboard, get_offer_traffic_type_keayboard
from robot.utils.db_api import get_offers_by_data

# FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ChooseOffer(StatesGroup):
    category = State()
    geo = State()
    traffic_type = State()


@dp.callback_query_handler(lambda call: call.data.startswith('offers'))
async def language_change(call: types.CallbackQuery):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    # state FSM to category
    await ChooseOffer.category.set()

    await call.answer('')
    await call.message.answer(
        text=await get_bot_text(f'offers clicked {telegram_user.lang}'),
        reply_markup=await get_offer_type_keayboard(),
    )


@dp.callback_query_handler(lambda call: call.data.startswith('category_offer_chosen'), state=ChooseOffer.category)
async def category_offer_chosen(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    chosen_category = call.data.split(':')[-1]
    logging.info(f'Chosen category: {chosen_category}')

    # update state in FSM
    # change it to geo
    async with state.proxy() as data:
        data['category'] = chosen_category
    await ChooseOffer.geo.set()

    await call.answer('')
    await call.message.answer(
        text=await get_bot_text(f'offers category chosen {telegram_user.lang}'),
        reply_markup=await get_offer_geo_keayboard(),
    )


@dp.callback_query_handler(lambda call: call.data.startswith('geo_offer_chosen'), state=ChooseOffer.geo)
async def geo_offer_chosen(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    chosen_geo = call.data.split(':')[-1]
    logging.info(f'Chosen geo: {chosen_geo}')

    # update state in FSM
    # change it to traffic_type
    async with state.proxy() as data:
        data['geo'] = chosen_geo
    await ChooseOffer.traffic_type.set()

    await call.answer('')
    await call.message.answer(
        text=await get_bot_text(f'offers geo chosen {telegram_user.lang}'),
        reply_markup=await get_offer_traffic_type_keayboard(),
    )

# !!! FINISH


@dp.callback_query_handler(lambda call: call.data.startswith('traffic_type_offer_chosen'), state=ChooseOffer.traffic_type)
async def traffic_type_offer_chosen(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    chosen_traffic_type = call.data.split(':')[-1]
    logging.info(f'Chosen traffic_type: {chosen_traffic_type}')

    # update state in FSM
    # change it to traffic_type
    async with state.proxy() as data:
        data['traffic_type'] = chosen_traffic_type
        
        logging.info(f'Offer data: {data}')
        
        offer_by_data = await get_offers_by_data(data)
        
        for offer in offer_by_data:
            
            if telegram_user.lang == 'ru':
                text = ""
                
                text += f'Название оффера: {offer.name}\n' + \
                    f'Гео: {offer.geo}\n' + \
                        f'Тип трафика: {offer.traffic_type}\n'
                        
                kb = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text='Перейти к офферу', url=offer.offer_link)]
                ])

                await call.answer('')
                await call.bot.send_message(
                    chat_id=call.from_user.id,
                    text=text,
                    reply_markup=kb,
                )
            else:
                text = ""
                
                text += f'Offer name: {offer.name}\n' + \
                    f'Geo: {offer.geo}\n' + \
                        f'Traffic type: {offer.traffic_type}\n'
                        
                kb = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text='Go to offer', url=offer.offer_link)]
                ])

                await call.answer('')
                await call.bot.send_message(
                    chat_id=call.from_user.id,
                    text=text,
                    reply_markup=kb,
                )

    await state.finish()
