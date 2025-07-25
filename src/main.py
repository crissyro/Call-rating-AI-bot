import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from config.config import settings
from core.logger import setup_logger, LoggingMiddleware
from services.analyzer import CallAnalyzer
from handlers.analysis import analysis_router

async def main():
    logger = setup_logger()

    bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    logging_middleware = LoggingMiddleware(logger)
    dp.update.outer_middleware(logging_middleware)
    
    dp.include_router(analysis_router)
    
    logger.info("Bot is starting polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())