##
# @file main.py
# @author Roman Moroz
# @brief Главная точка входа для запуска Telegram-бота.
# @details Этот скрипт отвечает за инициализацию всех ключевых компонентов приложения:
#          логгера, бота, диспетчера, а также за регистрацию "middleware" и роутеров.
#          После завершения настройки он запускает бота в режиме long-polling.

import asyncio
import logging
from aiogram import Bot, Dispatcher

from config.config import settings
from core.logger import setup_logger, LoggingMiddleware
from handlers.analysis import analysis_router


async def main():
    """!
    @brief Основная асинхронная функция для инициализации и запуска бота.
    @details
    Выполняет последовательность действий для сборки и запуска приложения:
    1. Инициализирует глобальный логгер с помощью `setup_logger`.
    2. Создает экземпляр `Bot` с токеном из файла конфигурации.
    3. Создает экземпляр `Dispatcher` для обработки входящих обновлений.
    4. Регистрирует `LoggingMiddleware` как "внешний" middleware (outer_middleware).
       Это позволяет логировать и безопасно обрабатывать ошибки для всех без исключения событий.
    5. Подключает к главному диспетчеру все обработчики команд и сообщений из `analysis_router`.
    6. Удаляет любые предыдущие настройки вебхука для чистого запуска в режиме поллинга.
    7. Запускает бесконечный цикл получения обновлений от Telegram (long-polling).
    """

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
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger("call_assessment_bot").info("Bot stopped manually.")
