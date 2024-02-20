import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

from config_reader import config
from handlers import setup_message_routers
from middlewares import ThrottlingMiddleware


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.message.middleware(ThrottlingMiddleware())

    message_routers = setup_message_routers()
    dp.include_router(message_routers)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
