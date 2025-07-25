##
# @file analysis.py
# @author Roman Moroz
# @brief Модуль для обработки сообщений и команд от пользователя в Telegram.
# @details Этот файл содержит всю логику, связанную с прямым взаимодействием с
#          пользователем. Он определяет, как бот реагирует на команду `/start`,
#          на текстовые сообщения и на неподдерживаемый контент.
#          Основной принцип работы - принять запрос, провести базовую валидацию
#          и передать "тяжелую" работу по анализу текста в сервисный модуль `analyzer`.

import logging

from aiogram import Router, F, types
from aiogram.filters import CommandStart

from services.analyzer import analyzer

logger = logging.getLogger("call_assessment_bot")

##
# @var analysis_router
# @brief Экземпляр `aiogram.Router` для этого модуля.
# @details Этот роутер собирает все обработчики (хендлеры), определенные в этом файле.
#          Затем он импортируется и подключается к главному диспетчеру в `main.py`,
#          что обеспечивает модульность и чистоту кода.
analysis_router = Router()


@analysis_router.message(CommandStart())
async def cmd_start(message: types.Message):
    """!
    @brief Обработчик команды `/start`.
    @details
    Этот хендлер активируется, когда пользователь впервые запускает бота или
    отправляет команду `/start`. Он отправляет приветственное сообщение,
    представляется и объясняет свою основную функцию.
    @param message [in] Объект `aiogram.types.Message`, содержащий информацию о сообщении и пользователе.
    """

    welcome_text = (
        f"👋 **Привет, {message.from_user.full_name}!**\n\n"
        "Я — ИИ-агент по оценке звонков. "
        "Отправьте мне расшифровку телефонного разговора, "
        "и я определю его тон и дам две рекомендации по улучшению."
    )
    await message.answer(welcome_text, parse_mode="Markdown")


@analysis_router.message(F.text)
async def handle_text_message(message: types.Message):
    """!
    @brief Основной рабочий хендлер, который анализирует текстовые сообщения.
    @details
    Этот хендлер срабатывает на любое входящее текстовое сообщение благодаря фильтру `F.text`.
    Логика его работы следующая:
    1.  <b>Валидация:</b> Проверяет, что текст не слишком короткий (минимум 10 слов).
        Если проверка не пройдена, информирует пользователя и прекращает выполнение.
    2.  <b>Обратная связь:</b> Немедленно отправляет пользователю сообщение "Анализирую...",
        чтобы показать, что запрос принят в работу. Это улучшает пользовательский опыт.
    3.  <b>Делегирование:</b> Вызывает асинхронный метод `analyze_call` из импортированного
        сервиса `analyzer`, передавая ему текст сообщения. Вся сложная логика анализа
        инкапсулирована там.
    4.  <b>Отображение результата:</b> После получения результата от `analyzer`, редактирует
        ранее отправленное сообщение "Анализирую...", заменяя его на финальный отчет.
        Это позволяет избежать "засорения" чата лишними сообщениями.
    5.  <b>Приглашение к действию:</b> Сообщает пользователю, что готов к следующему заданию.
    @param message [in] Объект `aiogram.types.Message` с текстом для анализа.
    """

    if not message.text or len(message.text.split()) < 10:
        await message.answer(
            "⚠️ Текст слишком короткий. Для качественного анализа нужно минимум 10 слов."
        )
        return

    processing_msg = await message.answer(
        "🔍 Анализирую диалог... Это может занять до 30 секунд."
    )
    logger.info(
        f"Started analysis for user {message.from_user.id}. Text length: {len(message.text)}"
    )

    analysis_result = await analyzer.analyze_call(message.text)

    await processing_msg.edit_text(analysis_result, parse_mode="Markdown")

    logger.info(f"Finished analysis for user {message.from_user.id}")
    await message.answer("Готов к анализу следующего диалога!")


@analysis_router.message(F.content_type.is_not(types.ContentType.TEXT))
async def handle_unsupported_message(message: types.Message):
    """!
    @brief Обработчик для неподдерживаемых типов сообщений.
    @details
    Этот хендлер использует "магический" фильтр `F.content_type.is_not(...)` для
    перехвата всех сообщений, которые НЕ являются текстом (например, фото, стикеры,
    аудио, документы и т.д.). Он вежливо сообщает пользователю о том, что бот
    умеет работать только с текстом.
    """

    await message.answer("❌ Я умею анализировать только текстовые сообщения.")
