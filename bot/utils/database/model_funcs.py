from sqlalchemy import select

from bot import Session
from bot.utils.database.models import Subscriber, Searching, User, Tariff


async def get_or_create(model, **kwargs):
    async with Session() as session:
        result = await session.execute(select(User).filter_by(**kwargs))
        instance = result.scalars().first()
        if instance:
            return instance, False
        else:
            instance = model(**kwargs)
            session.add(instance)
            await session.commit()
            return instance, True


async def check_subscribe(user_id):
    async with Session() as session:
        result = await session.execute(select(Subscriber).join(User).filter(User.tg_id == user_id))
        subscriber = result.scalars().first()
        return subscriber is not None


async def check_start(user_id):
    async with Session() as session:
        result = await session.execute(select(Searching).join(User).filter(User.tg_id == user_id))
        search = result.scalars().first()
        return search is not None and search.start


async def get_tariff(user_id):
    async with Session() as session:
        result = await session.execute(select(Subscriber).join(User).filter(User.tg_id == user_id))
        tariff = result.scalars().first()
        return tariff


async def get_all_tariff():
    async with Session() as session:
        result = await session.execute(select(Tariff))
        return result.scalars().all()
