from datetime import date

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.states.menus import MainMenu, PersonalAreaWithAccess, PersonalAreaWithoutAccess
from bot.utils.buttons import back_btn, main_menu_btn, get_main_menu_btn
from bot.utils.database.model_funcs import get_or_create, check_subscribe, check_start, get_tariff, get_all_tariff
from bot.utils.database.models import User


async def send_main_menu_call(query: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=1)
    text = "Тестовое главное меню"
    all_buttons = await get_main_menu_btn(query.message.chat.id)
    markup.add(*all_buttons)
    await MainMenu.first()
    await query.message.edit_text(
        text=text,
        reply_markup=markup,
    )


async def send_main_menu_msg(message: Message, state: FSMContext):
    await get_or_create(User, tg_id=message.from_id,
                        username=message.from_user.username if message.from_user.username else None)
    markup = InlineKeyboardMarkup(row_width=1)
    text = "Тестовое главное меню"
    all_buttons = await get_main_menu_btn(message.from_id)
    markup.add(*all_buttons)
    await MainMenu.first()
    await message.answer(text, reply_markup=markup)


async def check_date(future_date):
    days_left = (future_date - date.today()).days
    if days_left % 10 == 1 and days_left % 100 != 11:
        days_word = "день"
    elif days_left % 10 in [2, 3, 4] and days_left % 100 not in [12, 13, 14]:
        days_word = "дня"
    else:
        days_word = "дней"
    left_word = "осталось" if days_left % 10 == 1 and days_left % 100 != 11 else "осталось"
    return days_word, left_word, days_left


async def personal_area(query: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup()
    if await check_subscribe(query.from_user.id):
        tariff = await get_tariff(query.from_user.id)
        days_word, left_word, days_left = await check_date(tariff.date_end_subscribe)
        text = f"Ваш тариф - {tariff.tariff.name}\n\n" \
               f"Оплачено до - {tariff.date_end_subscribe}\n\n" \
               f"У вас {left_word} {days_left} {days_word}"
        await PersonalAreaWithAccess.first()
    else:
        text = "У вас не приобретен доступ к боту. Ознакомьтесь со списком тарифов и выберите подходящий!"
        markup.add(*[InlineKeyboardButton(text=tariff.name, callback_data=f"tariff_{tariff.id}") for tariff in
                     await get_all_tariff()])
        await PersonalAreaWithoutAccess.first()
    markup.add(back_btn, main_menu_btn)
    await query.message.edit_text(text, reply_markup=markup)
