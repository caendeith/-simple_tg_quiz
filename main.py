import asyncio
import logging
from aiogram import Bot, Dispatcher
from database import create_table
from handlers import router as handlers_router
from callbacks import router as callbacks_router

logging.basicConfig(level=logging.INFO)
API_TOKEN = 'YOUR_BOT_TOKEN'

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(handlers_router)
    dp.include_router(callbacks_router)
    
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())