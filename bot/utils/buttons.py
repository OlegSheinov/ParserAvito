from aiogram.types import InlineKeyboardButton

from bot.utils.database.model_funcs import check_subscribe, check_start

back_btn = InlineKeyboardButton(text="Назад", callback_data="back")
main_menu_btn = InlineKeyboardButton(text="В главное меню", callback_data="main_menu")


async def get_main_menu_btn(user_id):
    all_buttons = [
        InlineKeyboardButton(text="Личный кабинет", callback_data="personal_area"),
        InlineKeyboardButton(text="Изменить параметры парсинга", callback_data="parsing_options"),
        InlineKeyboardButton(text="Инструкция", callback_data="instruction"),
        InlineKeyboardButton(text="Поддержка", callback_data="support"),
    ]
    if await check_subscribe(user_id):
        all_buttons.insert(
            1,
            InlineKeyboardButton(
                text="Остановить поиск" if await check_start(user_id) else "Запустить поиск",
                callback_data="stop" if await check_start(user_id) else "start"
            )
        )
    return all_buttons
