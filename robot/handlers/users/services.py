import logging
from robot.models import TelegramUser, Service
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from get_bot_info import get_bot_text
from robot.keyboards.default import get_offer_type_keayboard, get_back_kb, get_services_result_kb, get_service_type_keyboard
from robot.utils.db_api import get_services_by_category

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ChooseService(StatesGroup):
    category = State()


@dp.callback_query_handler(lambda call: call.data.startswith('services'), state='*')
async def services_start(call: types.CallbackQuery):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)
    await ChooseService.category.set()

    await call.answer('')
    await call.message.edit_text(
        text=await get_bot_text(f'services clicked {telegram_user.lang}'),
        reply_markup=await get_service_type_keyboard(),
        parse_mode='Markdown'
    )


@dp.callback_query_handler(lambda call: call.data.startswith('category_service_chosen'), state=ChooseService.category)
async def service_category_chosen(call: types.CallbackQuery, state: FSMContext):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    chosen_category = call.data.split(':')[-1]

    if chosen_category != 'continue':
        async with state.proxy() as data:
            arr = data.get('category', [])
            if chosen_category in arr:
                arr.remove(chosen_category)
            else:
                arr.append(chosen_category)
            data['category'] = arr

        await call.message.edit_text(
            text=await get_bot_text(f'services clicked {telegram_user.lang}'),
            reply_markup=await get_service_type_keyboard(arr),
            parse_mode='Markdown'
        )
    else:
        async with state.proxy() as data:
            services = await get_services_by_category(data.get('category', []))

            if not services:
                text = "По вашему запросу ничего не найдено" if telegram_user.lang == 'ru' else "Nothing found by your request"
                await call.message.edit_text(
                    text=text,
                    reply_markup=await get_back_kb(),
                )
                await state.finish()
                return

            await state.update_data(services=services)
            await state.update_data(service_page=0)

            await call.message.edit_text(
                text=await get_bot_text(f'services list {telegram_user.lang}'),
                reply_markup=await get_services_result_kb(services, 0),
                parse_mode='Markdown'
            )


@dp.callback_query_handler(lambda call: call.data.startswith('service_get_id'), state=ChooseService.category)
async def service_get_id(call: types.CallbackQuery, state: FSMContext):
    await call.answer('')
    service_id = call.data.split(':')[-1]
    service = await Service.objects.aget(id=service_id)
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    service_text = f'Название сервиса: {service.name}\n\nКатегория сервиса: {service.category}' \
        if telegram_user.lang == 'ru' else \
        f'Service name: {service.name}\n\nService category: {service.category}'

    await call.message.edit_text(
        text=service_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    url=service.url,
                    text='Перейти к сервису' if telegram_user.lang == 'ru' else 'Go to service')],
                [InlineKeyboardButton(
                    text='🔙 Back',
                    callback_data='back_to_services')]
            ]
        ),
        parse_mode='Markdown'
    )


@dp.callback_query_handler(lambda call: call.data.startswith('service_prev_page'), state=ChooseService.category)
async def service_prev_page(call: types.CallbackQuery, state: FSMContext):
    await call.answer('')
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)
    async with state.proxy() as data:
        services = data.get('services', [])
        page = data.get('service_page', 0)
        page = max(0, page - 1)
        data['service_page'] = page

        await call.message.edit_text(
            text=await get_bot_text(f'services list {telegram_user.lang}'),
            reply_markup=await get_services_result_kb(services, page),
            parse_mode='Markdown'
        )


@dp.callback_query_handler(lambda call: call.data.startswith('service_next_page'), state=ChooseService.category)
async def service_next_page(call: types.CallbackQuery, state: FSMContext):
    await call.answer('')
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)
    async with state.proxy() as data:
        services = data.get('services', [])
        page = data.get('service_page', 0)
        page = min(len(services) - 1, page + 1)
        data['service_page'] = page

        await call.message.edit_text(
            text=await get_bot_text(f'services list {telegram_user.lang}'),
            reply_markup=await get_services_result_kb(services, page),
            parse_mode='Markdown'
        )


@dp.callback_query_handler(lambda call: call.data.startswith('back_to_services'), state=ChooseService.category)
async def back_to_services(call: types.CallbackQuery, state: FSMContext):
    await call.answer('')
    telegram_user, _ = await TelegramUser.objects.aget_or_create(chat_id=call.from_user.id)

    async with state.proxy() as data:
        services = data.get('services', [])
        page = data.get('service_page', 0)

    await call.message.edit_text(
        text=await get_bot_text(f'services clicked {telegram_user.lang}'),
        reply_markup=await get_services_result_kb(services, page),
        parse_mode='Markdown'
    )
