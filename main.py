import asyncio
import logging
from loader import bot, dp
from database.models import async_main
from handlers import common, search, booking, favorites
from dotenv import load_dotenv
load_dotenv()



async def main():
    logging.basicConfig(level=logging.INFO)
    await async_main()
    print("База данных подключена.")
    dp.include_router(common.router)
    dp.include_router(search.router)
    dp.include_router(favorites.router)
    dp.include_router(booking.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
