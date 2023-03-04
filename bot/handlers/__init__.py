from aiogram import Dispatcher

from bot.handlers.main_menu import send_main_menu_msg, personal_area, send_main_menu_call
from bot.handlers.parsing_options import request_city_name, get_city_name_and_offer_location, request_location, \
    get_location_and_request_radius, get_radius_and_request_category, get_category_and_request_subcategory, \
    get_location_and_request_radius_call
from bot.states.menus import MainMenu
from bot.states.scenarios import ParsingOptions


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_main_menu_msg, state="*", commands=['start'])
    dp.register_callback_query_handler(send_main_menu_call, lambda query: 'main_menu' == query.data, state="*")
    dp.register_callback_query_handler(personal_area, lambda query: 'personal_area' == query.data,
                                       state=MainMenu.main_menu)


def register_scenario_options(dp: Dispatcher):
    dp.register_callback_query_handler(request_city_name, lambda query: "parsing_options" == query.data,
                                       state=MainMenu.main_menu)
    dp.register_message_handler(get_city_name_and_offer_location, state=ParsingOptions.city)
    dp.register_callback_query_handler(request_location, lambda query: "Yes" == query.data,
                                       state=ParsingOptions.location)
    dp.register_message_handler(get_location_and_request_radius, content_types=['location'],
                                state=ParsingOptions.radius)
    dp.register_callback_query_handler(get_location_and_request_radius_call, lambda query: "Not" == query.data,
                                       state=ParsingOptions.location)
    dp.register_message_handler(get_radius_and_request_category, state=ParsingOptions.category)
    dp.register_callback_query_handler(get_category_and_request_subcategory, lambda query: "category_" in query.data,
                                       state=ParsingOptions.category)
