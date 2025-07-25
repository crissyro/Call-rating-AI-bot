import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config.config import config
from core.logger import setup_logger, LoggingMiddleware

logger = setup_logger()

bot = Bot(token=config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    logger.info(f"User {user.id} started bot", extra={'user': f"{user.id} ({user.username})"})
    
    welcome_text = (
        f"✨ Привет, {user.full_name}!\n\n"
    )
    
    await message.answer(welcome_text)

async def main():
    logging_middleware = LoggingMiddleware(logger)
    dp.update.outer_middleware(logging_middleware)
    
    logger.info("Starting Mood Journal Bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())