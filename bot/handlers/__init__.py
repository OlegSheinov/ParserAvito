from aiogram import Dispatcher

from bot.handlers.main_menu import send_main_menu_msg, personal_area, send_main_menu_call
from bot.handlers.parsing_options import request_city_name, get_city_name_and_offer_location, request_location, \
    get_location_and_request_radius, get_radius_and_request_category, get_category_and_request_subcategory, \
    get_location_and_request_radius_call, get_subcategory_and_offer_filters, get_filters_and_request_keyword, \
    get_ad_type_and_send_result, get_keyword_and_request_ad_type
from bot.states.menus import MainMenu
from bot.states.scenarios import ParsingOptions


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_main_menu_msg, state="*", commands=['start'])
    dp.register_callback_query_handler(send_main_menu_call, lambda q: 'main_menu' == q.data, state="*")
    dp.register_callback_query_handler(personal_area, lambda q: 'personal_area' == q.data,
                                       state=MainMenu.main_menu)


def register_scenario_options(dp: Dispatcher):
    dp.register_callback_query_handler(request_city_name, lambda q: "parsing_options" == q.data,
                                       state=MainMenu.main_menu)
    dp.register_message_handler(get_city_name_and_offer_location, state=ParsingOptions.city)
    dp.register_callback_query_handler(request_location, lambda q: "Yes" == q.data,
                                       state=ParsingOptions.location)
    dp.register_callback_query_handler(get_location_and_request_radius_call, lambda q: "Not" == q.data,
                                       state=ParsingOptions.location)
    dp.register_message_handler(get_location_and_request_radius, content_types=['location'],
                                state=ParsingOptions.radius)
    dp.register_message_handler(get_radius_and_request_category, state=ParsingOptions.category)
    dp.register_callback_query_handler(get_category_and_request_subcategory, lambda q: "category_" in q.data,
                                       state=ParsingOptions.category)
    dp.register_callback_query_handler(get_subcategory_and_offer_filters, lambda q: "Yes" == q.data,
                                       state=ParsingOptions.subcategory)
    dp.register_callback_query_handler(get_filters_and_request_keyword, lambda q: "Not" == q.data,
                                       state=ParsingOptions.subcategory)

    dp.register_callback_query_handler(get_subcategory_and_offer_filters, lambda q: "Yes" == q.data,
                                       state=ParsingOptions.additional_filters)
    dp.register_callback_query_handler(get_filters_and_request_keyword,
                                       lambda q: (q.data == "Not") | (q.data == "Ready"),
                                       state=ParsingOptions.additional_filters)

    dp.register_callback_query_handler(get_keyword_and_request_ad_type, lambda q: "Yes" == q.data,
                                       state=ParsingOptions.keywords)
    dp.register_callback_query_handler(get_ad_type_and_send_result, lambda q: "Not" == q.data,
                                       state=ParsingOptions.keywords)

    dp.register_callback_query_handler(get_ad_type_and_send_result, state=ParsingOptions.ad_type)
