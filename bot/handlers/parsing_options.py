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
                        data.update(city_id=city_id['id'])
                    await ParsingOptions.next()
                    print(data)
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


async def get_location_and_request_radius(message: Message, state: FSMContext):
    text = 'Пожалуйста, введите радиус в км от вашего местоположения!'
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await ParsingOptions.next()


async def get_radius_and_request_category(message: Message, state: FSMContext):
    text = "Выберите категорию, которая вас интересует!"
    async with state.proxy() as data:
        if data.get('get_location'):
            data.update(radius=int(message.text))
            body = {
                "locationId": data.get('city_id'),
                "geoCoords": [data.get('x'), data.get('y')],
                "radius": data.get('radius')
            }
            await ParsingOptions.next()
        else:
            body = {
                "locationId": data.get('city_id')
            }
            await state.set_state(ParsingOptions.category)
    markup = InlineKeyboardMarkup(row_width=2)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/get_main_categories/', json=body) as response:
            categories = await response.json()
    markup.add(
        *[InlineKeyboardButton(text=category['title'], callback_data=f"category_{category['id']}") for category in
          categories])
    if isinstance(message, CallbackQuery):
        return await message.message.edit_text(text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)


async def get_category_and_request_subcategory(query: CallbackQuery, state: FSMContext):
    text = "Выберите подкатегорию, которая вас интересует!"
    async with state.proxy() as data:
        data.update(categoryId=int(query.data.split("category_")[1]))
        if data.get('get_location'):
            body = {
                "locationId": data.get('city_id'),
                "geoCoords": [data.get('x'), data.get('y')],
                "radius": data.get('radius'),
                "categoryId": data.get('categoryId')
            }
        else:
            body = {
                "locationId": data.get('city_id'),
                "categoryId": data.get('categoryId')
            }
    markup = InlineKeyboardMarkup(row_width=2)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/get_subcategories/', json=body) as response:
            subcategories = await response.json()
    markup.add(
        *[InlineKeyboardButton(text=category['title'], callback_data=f"category_{category['id']}") for category in
          subcategories])
    await ParsingOptions.next()
    await query.message.edit_text(text, reply_markup=markup)


async def get_subcategory_and_offer_filters(query: CallbackQuery, state: FSMContext):
    pass


async def choice_keywords(query: CallbackQuery, state: FSMContext):
    pass


async def choice_ad_type(message: Message, state: FSMContext):
    pass


async def result(query: CallbackQuery, state: FSMContext):
    pass
