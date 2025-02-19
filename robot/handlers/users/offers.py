import logging

from robot.models import TelegramUser, Offer
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from get_bot_info import get_bot_text
from robot.keyboards.default import get_offer_type_keayboard, get_offer_geo_keayboard, get_offer_traffic_type_keayboard, get_back_kb, get_offers_result_kb
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
            if chosen_category in arr:
                arr.remove(chosen_category)
            else:
                arr.append(chosen_category)
            data['category'] = arr

            logging.info(f'Offer data: {arr}')

        await call.answer('')
        await call.message.edit_text(
            text=await get_bot_text(f'offers clicked {telegram_user.lang}'),
            reply_markup=await get_offer_type_keayboard(arr),
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
            if chosen_geo in arr:
                arr.remove(chosen_geo)
            else:
                arr.append(chosen_geo)
            data['geo'] = arr

            logging.info(f'Offer data: {arr}')

        await call.answer('')
        await call.message.edit_text(
            text=await get_bot_text(f'offers category chosen {telegram_user.lang}'),
            reply_markup=await get_offer_geo_keayboard(arr),
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
            if chosen_traffic_type in arr:
                arr.remove(chosen_traffic_type)
            else:
                arr.append(chosen_traffic_type)
            data['traffic_type'] = arr

            logging.info(f'Offer data: {arr}')

            await call.answer('')
            await call.message.edit_text(
                text=await get_bot_text(f'offers geo chosen {telegram_user.lang}'),
                reply_markup=await get_offer_traffic_type_keayboard(arr),
                parse_mode='Markdown'
            )
    else:
        await call.answer('')
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
            else:
                # save offer_by_data to state
                await state.update_data(offer_by_data=offer_by_data)
                await state.update_data(offer_page=0)

            await call.message.edit_text(
                text=await get_bot_text(f'offers list {telegram_user.lang}'),
                reply_markup=await get_offers_result_kb(offer_by_data, (await state.get_data())['offer_page']),
                parse_mode='Markdown'
            )


@dp.callback_query_handler(lambda call: call.data.startswith('offer_next_page'), state=ChooseOffer.traffic_type)
async def offer_next_page(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    await call.answer('')
    offer_by_data = (await state.get_data())['offer_by_data']

    async with state.proxy() as data:
        if (await state.get_data())['offer_page'] < len(offer_by_data) / 5:
            data['offer_page'] += 1
            await call.answer('')
        else:
            await call.answer('Это последняя страница' if telegram_user.lang == 'ru' else 'This is the last page')

    await call.message.edit_text(
        text=await get_bot_text(f'offers list {telegram_user.lang}'),
        reply_markup=await get_offers_result_kb(offer_by_data, (await state.get_data())['offer_page']),
        parse_mode='Markdown'
    )


@dp.callback_query_handler(lambda call: call.data.startswith('offer_prev_page'), state=ChooseOffer.traffic_type)
async def offer_prev_page(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    async with state.proxy() as data:
        if (await state.get_data())['offer_page'] > 0:
            data['offer_page'] -= 1
            await call.answer('')
        else:
            await call.answer('Это первая страница' if telegram_user.lang == 'ru' else 'This is the first page')

    offer_by_data = (await state.get_data())['offer_by_data']

    await call.message.edit_text(
        text=await get_bot_text(f'offers list {telegram_user.lang}'),
        reply_markup=await get_offers_result_kb(offer_by_data, (await state.get_data())['offer_page']),
        parse_mode='Markdown'
    )


@dp.callback_query_handler(lambda call: call.data.startswith('offer_get_id'), state=ChooseOffer.traffic_type)
async def offer_get_id(call: types.CallbackQuery, state: FSMContext):
    await call.answer('')
    offer_id = call.data.split(':')[-1]
    offer = await Offer.objects.aget(id=offer_id)
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    if telegram_user.lang == 'ru':
        offer_text = f'Название офера: {offer.name}\n\nКатегория офера: {offer.category}\n\nГео: {offer.geo}\n\nТрафик: {offer.traffic_type}\n\nСсылка на офер: {offer.offer_link}'
    else:
        offer_text = f'Offer name: {offer.name}\n\nOffer category: {offer.category}\n\nOffer geo: {offer.geo}\n\nOffer traffic: {offer.traffic_type}\n\nOffer link: {offer.offer_link}'

    await call.message.edit_text(
        text=offer_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    url=offer.offer_link, text='Перейти к оферу' if telegram_user.lang == 'ru' else 'Go to offer')],
                [InlineKeyboardButton(
                    text='🔙 Back', callback_data='back_to_offers')]
            ]
        ),
        parse_mode='Markdown'
    )


@dp.callback_query_handler(lambda call: call.data.startswith('back_to_offers'), state=ChooseOffer.traffic_type)
async def back_to_offers(call: types.CallbackQuery, state: FSMContext):
    await call.answer('')
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    offer_by_data = (await state.get_data())['offer_by_data']

    await call.message.edit_text(
        text=await get_bot_text(f'offers list {telegram_user.lang}'),
        reply_markup=await get_offers_result_kb(offer_by_data, (await state.get_data())['offer_page']),
        parse_mode='Markdown'
    )
