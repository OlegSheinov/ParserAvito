from aiogram.dispatcher.filters.state import StatesGroup, State


class ParsingOptions(StatesGroup):
    city = State()
    location = State()
    radius = State()
    category = State()
    subcategory = State()
    additional_filters = State()
    keywords = State()
    ad_type = State()
    result = State()
