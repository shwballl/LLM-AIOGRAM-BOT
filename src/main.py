import os
from dotenv import load_dotenv
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .app.handlers import router
from .logger_config import configure_logging, LogLevels


load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")

async def main() -> None:
    """The main entry point of the bot. Sets up the Dispatcher and starts it."""
    
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    configure_logging(LogLevels.info)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass