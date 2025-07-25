##
# @file logger.py
# @author Ваш Никнейм
# @brief Модуль для централизованной настройки логирования и обработки ошибок в приложении.
# @details Этот файл содержит две ключевые части:
#          1. `setup_logger()`: Функция для инициализации и конфигурации глобального логгера.
#          2. `LoggingMiddleware`: Класс middleware для `aiogram`, который перехватывает
#             все входящие события для их логирования и централизованно обрабатывает
#             любые исключения, возникающие в хендлерах, предотвращая падение бота.

import logging
import sys

from pathlib import Path
from logging import Formatter, StreamHandler
from colorlog import ColoredFormatter

def setup_logger() -> logging.Logger:
    """!
    @brief Инициализирует и настраивает главный логгер приложения.
    @details
    Создает и конфигурирует именованный логгер (`call_assessment_bot`). Настройка
    включает два обработчика (handlers):
    - <b>Консольный обработчик:</b> Выводит логи всех уровней (от DEBUG и выше) в
      консоль с использованием цветного форматирования для лучшей читаемости
      во время разработки. Использует библиотеку `colorlog`.
    - <b>Файловый обработчик:</b> Записывает логи уровня INFO и выше в файл `logs/bot.log`.
      Это позволяет сохранять важную информацию о работе бота в продакшене,
      исключая отладочные сообщения.
    
    Функция также автоматически создает директорию `logs`, если она не существует.
    @note Эту функцию следует вызывать только один раз при старте приложения (в `main.py`),
          чтобы избежать дублирования обработчиков и многократной записи одних и тех же логов.
          Тестовые сообщения в конце функции служат для проверки корректности настройки
          при первом запуске.
    @return logging.Logger: Полностью настроенный экземпляр логгера.
    """
    
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "bot.log"
    
    logger = logging.getLogger("call_assessment_bot")
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()
    
    console_format = (
        "%(log_color)s[%(asctime)s] %(blue)s%(name)s:%(reset)s "
        "%(log_color)s%(levelname)s%(reset)s | "
        "%(cyan)s%(funcName)s:%(reset)s %(log_color)s%(message)s"
    )
    
    console_formatter = ColoredFormatter(
        console_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_purple',
        },
        secondary_log_colors={},
        style='%'
    )
    
    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_formatter = Formatter(
        "[%(asctime)s] %(name)s:%(levelname)s | %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logger.debug("Debug message test")
    logger.info("Info message test")
    logger.warning("Warning message test")
    logger.error("Error message test")
    logger.critical("Critical message test")
    
    return logger

class LoggingMiddleware:
    """!
    @class LoggingMiddleware
    @brief Middleware для `aiogram` для логирования всех событий и глобальной обработки ошибок.
    @details
    Этот класс является "внешним" middleware (outer middleware), который оборачивает
    обработку каждого входящего события (сообщения, нажатия кнопок и т.д.).
    
    Его задачи:
    1. Логировать информацию о событии и пользователе до того, как оно будет передано
       в соответствующий хендлер.
    2. Выполнять хендлер внутри блока `try...except`, чтобы перехватывать любые
       необработанные исключения. Это действует как "защитная сетка" (safety net)
       для всего бота, предотвращая его остановку из-за ошибки в одном из хендлеров.
    3. В случае ошибки, логировать полную информацию об исключении и отправлять
       пользователю вежливое сообщение о сбое.
    """
    
    def __init__(self, logger):
        """!
        @brief Конструктор middleware.
        @details Принимает экземпляр логгера через механизм внедрения зависимостей.
        @param logger Экземпляр `logging.Logger`, который будет использоваться для записи логов.
        """
        
        self.logger = logger

    async def __call__(self, handler, event, data):
        """!
        @brief Основной асинхронный метод, вызываемый `aiogram` для каждого события.
        @param handler Следующий обработчик в цепочке вызовов.
        @param event Объект события (например, `types.Message` или `types.CallbackQuery`).
        @param data Словарь с дополнительными данными, передаваемыми по цепочке middleware.
        @return Возвращает результат выполнения `handler` или `True`, если было перехвачено исключение.
        @warning В блоке `except` возвращается `True`. Это критически важно для `aiogram`,
                 так как это сигнализирует диспетчеру, что ошибка была обработана и не
                 нужно ее распространять дальше, что предотвращает остановку бота.
        """
        
        user = data.get("event_from_user")
        user_info = f"{user.id} ({user.username})" if user else "Unknown"
        
        self.logger.info(
            f"Processing {type(event).__name__} from {user_info}",
            extra={'user': user_info}
        )
        
        try:
            return await handler(event, data)
        except Exception as e:
            self.logger.error(f"Error in handler for {type(event).__name__}: {e}", exc_info=True)
            
            if hasattr(event, "answer"):
                 await event.answer("⚠️ Произошла внутренняя ошибка. Мы уже работаем над этим.")
                 
            return True