from aiogram.dispatcher.filters.state import StatesGroup, State


class MainMenu(StatesGroup):
    main_menu = State()


class PersonalAreaWithAccess(StatesGroup):
    main_menu = State()
    extend_tariff = State()
    change_tariff = State()


class PersonalAreaWithoutAccess(StatesGroup):
    main_menu = State()
    buy_tariff = State()


class Instruction(StatesGroup):
    main_menu = State()


class Support(StatesGroup):
    main_menu = State()
    write_message = State()
