import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from database import create_table
from handlers import router as handlers_router
from callbacks import router as callbacks_router

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена бота из переменных окружения
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    logging.error("Не удалось найти API_TOKEN в переменных окружения или .env файле")
    exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(handlers_router)
    dp.include_router(callbacks_router)
    
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
