from logging.handlers import RotatingFileHandler
import logging
import asyncio

from aiogram import Bot, Dispatcher

from config_data.config import TOKEN
from handlers.message_handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


async def start():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # handler = RotatingFileHandler("app.log", maxBytes=100000, backupCount=3)
    # logging.basicConfig(handlers=[handler], level=logging.INFO,
    #                     format="%(asctime)s - %(name)s -"
    #                            " %(levelname)s - %(message)s")
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()
