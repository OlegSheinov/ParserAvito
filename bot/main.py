from aiogram import Dispatcher
from aiogram.utils import executor

from bot import log, create_bot, create_storage, create_dispatcher, loop, engine
from bot.handlers import register_handlers, register_scenario_options
from bot.utils.database.models import Base


async def test(dp: Dispatcher):
    register_handlers(dp)
    register_scenario_options(dp)


@log(info_message="Start Bot!")
async def startup(dispatcher: Dispatcher):
    await test(dispatcher)



@log(info_message="Stop Bot!")
async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    bot = create_bot()
    storage = create_storage()
    dp = create_dispatcher(bot, storage, loop)
    loop.run_until_complete(create_tables())
    executor.start_polling(dp, skip_updates=True, loop=loop, on_shutdown=shutdown, on_startup=startup)
