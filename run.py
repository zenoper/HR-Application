import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from app.middlewares import ThrottlingMiddleware
from utils.notify_admin import on_startup, on_shutdown
from utils.bot_commands import set_default_commands

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)
# run this bro


async def main():
    from app.handlers.start import entry_router
    await on_startup(bot)
    await set_default_commands(bot)

    dp.include_router(entry_router)
    dp.message.outer_middleware(ThrottlingMiddleware(limit=2, interval=1))
    await dp.start_polling(bot)
    await on_shutdown(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())