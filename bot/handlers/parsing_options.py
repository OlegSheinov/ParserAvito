import re

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove
from aiohttp import ClientSession

from bot.states.scenarios import ParsingOptions


async def request_city_name(query: CallbackQuery, state: FSMContext):
    text = "Введите название города/региона:"
    await ParsingOptions.first()
    await query.message.edit_text(text)


async def get_city_name_and_offer_location(message: Message, state: FSMContext):
    city = message.text
    body = {'name': city}
    markup = InlineKeyboardMarkup()
    async with ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/get_city_id/", json=body) as response:
            match response.status:
                case 200:
                    city_id = await response.json()
                    text = f"Хотите искать в определенном радиусе от вашего местоположения?"
                    markup.add(
                        InlineKeyboardButton(text="Да", callback_data="Yes"),
                        InlineKeyboardButton(text="Нет", callback_data="Not"),
                    )
                    async with state.proxy() as data:
                        data.update(locationId=city_id['id'])
                    await ParsingOptions.next()
                case 404:
                    text = "Введенный вами город не найден. Повторите попытку!"
                case _:
                    text = "Что-то пошло не так! Обратитесь в поддержку!"
    await message.answer(text, reply_markup=markup)


async def request_location(query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data.update(get_location=True)
    text = "Пожалуйста, вышлите ваше местоположение!"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(text="Отправить местоположение!", request_location=True))
    await ParsingOptions.next()
    await query.message.answer(text, reply_markup=markup)


async def get_location_and_request_radius_call(query: CallbackQuery, state: FSMContext):
    text = 'Пожалуйста, введите радиус в км от центра вашего города!(укажите 0, если искать во всем городе/регионе)'
    await query.message.edit_text(text)
    await state.set_state(ParsingOptions.category)


async def get_location_and_request_radius(message: Message, state: FSMContext):
    text = 'Пожалуйста, введите радиус в км от вашего местоположения!'
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await ParsingOptions.next()


async def get_radius_and_request_category(message: Message, state: FSMContext):
    text = "Выберите категорию, которая вас интересует!"
    async with state.proxy() as data:
        data.update(radius=int(message.text))
        await ParsingOptions.next()
        await state.set_state(ParsingOptions.category)
    body = data.as_dict()
    markup = InlineKeyboardMarkup(row_width=2)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/get_main_categories/', json=body) as response:
            categories = await response.json()
    markup.add(
        *[InlineKeyboardButton(text=category['name'], callback_data=f"_category_{category['id']}") for category in
          categories])
    if isinstance(message, CallbackQuery):
        return await message.message.edit_text(text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)


async def get_category_and_request_subcategory(query: CallbackQuery, state: FSMContext):
    text = "Выберите подкатегорию, которая вас интересует!"
    async with state.proxy() as data:
        category_match = re.search(r"category_(\d+)", query.data)
        data.update(categoryId=int(category_match.group(1)) if category_match else None)
        parent_match = re.search(r"parentId_(\d+)", query.data)
        data.update(parentId=int(parent_match.group(1)) if parent_match else None)
        params_match = re.search(r"\[\'(.*?)\'\]", query.data)
        data.update(params=params_match.group() if params_match else None)
    body = data.as_dict()
    markup = InlineKeyboardMarkup(row_width=2)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/get_subcategories/', json=body) as response:
            subcategories = await response.json()
    if not subcategories:
        await ParsingOptions.next()
        text = f"Хотите ли вы использовать дополнительные параметры поиска??"
        markup.add(
            InlineKeyboardButton(text="Да", callback_data="Yes"),
            InlineKeyboardButton(text="Нет", callback_data="Not"),
        )
    else:
        markup.add(
            *[InlineKeyboardButton(text=category['name'],
                                   callback_data=f"param_{category['param']}_parentId_{category['forParentId']}_category_{category['id']}")
              for category in
              subcategories])
    await query.message.edit_text(text, reply_markup=markup)


async def get_subcategory_and_offer_filters(query: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Все готово!", callback_data="Ready"),
    )
    text = "Тут список кнопок с доп фильтрами, которые будут перенаправлять на редактирование этих параметров. " \
           "Как это сделать, еще думаю"
    await ParsingOptions.next()
    await query.message.edit_text(text, reply_markup=markup)


async def get_filters_and_request_keyword(query: CallbackQuery, state: FSMContext):
    text = "Хотите ввести ключевые слова для поиска?"
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Да", callback_data="Yes"),
        InlineKeyboardButton(text="Нет", callback_data="Not"),
    )
    await ParsingOptions.next()
    await query.message.edit_text(text, reply_markup=markup)


async def get_keyword_and_request_ad_type(message: Message, state: FSMContext):
    text = "В каком виде вам выдавать объявления?"
    msg_simplified = "Упрощенное объявление с ссылкой"
    msg_full = "полное объявление с фото и тд"
    if isinstance(message, Message):
        await message.answer(msg_simplified)
        await message.answer(msg_full)
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text(msg_simplified)
        await message.message.edit_text(msg_full)
    else:
        pass
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Упрощенный", callback_data="Simplified"),
        InlineKeyboardButton(text="Полный", callback_data="Full"),
    )
    if isinstance(message, Message):
        await message.answer(text, reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text(text, reply_markup=markup)
    else:
        pass
    await ParsingOptions.next()


async def get_ad_type_and_send_result(query: CallbackQuery, state: FSMContext):
    text = f"Спасибо!\n Проверьте правильность вашего выбора:\n\n" \
           f"тут список того, что дал пользователь"
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text="Все верно!", callback_data="OK"))
    await query.message.edit_text(text, reply_markup=markup)
