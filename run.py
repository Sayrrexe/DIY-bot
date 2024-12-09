import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from tortoise import Tortoise

from app.user import user
from config import TOKEN, DB_URL
from app.database.init_db import create_data

logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def is_db_empty():
    # Проверка на пустоту базы данных (например, если нет записей в одной из таблиц)
    from app.database.models import Material

    count = await Material.all().count()
    return count == 0


async def startup(dispatcher: Dispatcher):
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["app.database.models"]},
    )
    await Tortoise.generate_schemas()

    if await is_db_empty():
        logger.info("База данных пуста. Инициализация...")
        await create_data()
    else:
        logger.info("БД уже заполнена!")


async def shutdown(dispatcher: Dispatcher):
    await Tortoise.close_connections()
    exit(0)


async def main():
    dp = Dispatcher()
    dp.include_router(user)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
