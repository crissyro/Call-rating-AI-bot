import logging

from aiogram import Router, F, types
from aiogram.filters import CommandStart

from services.analyzer import analyzer

logger = logging.getLogger("call_assessment_bot")
analysis_router = Router()

@analysis_router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработчик команды /start."""
    welcome_text = (
        f"👋 **Привет, {message.from_user.full_name}!**\n\n"
        "Я — ИИ-агент по оценке звонков. "
        "Отправьте мне расшифровку телефонного разговора, "
        "и я определю его тон и дам две рекомендации по улучшению."
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@analysis_router.message(F.text)
async def handle_text_message(message: types.Message):
    """Основной обработчик, принимающий текст для анализа."""

    if not message.text or len(message.text.split()) < 10:
        await message.answer("⚠️ Текст слишком короткий. Для качественного анализа нужно минимум 10 слов.")
        return

    processing_msg = await message.answer("🔍 Анализирую диалог... Это может занять до 40 секунд.")
    logger.info(f"Started analysis for user {message.from_user.id}. Text length: {len(message.text)}")

    analysis_result = await analyzer.analyze_call(message.text)
    
    await processing_msg.edit_text(analysis_result, parse_mode="Markdown")
    
    logger.info(f"Finished analysis for user {message.from_user.id}")
    await message.answer("Готов к анализу следующего диалога!")

@analysis_router.message(F.content_type.is_not(types.ContentType.TEXT))
async def handle_unsupported_message(message: types.Message):
    """Обработчик для сообщений, не являющихся текстом."""
    await message.answer("❌ Я умею анализировать только текстовые сообщения.")