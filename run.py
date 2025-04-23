import os
from dotenv import load_dotenv
import asyncio

from aiogram import Bot, Dispatcher

from logger_config import configure_logging, LogLevels
from app.handlers import router


load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")

async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    configure_logging(LogLevels.info)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass