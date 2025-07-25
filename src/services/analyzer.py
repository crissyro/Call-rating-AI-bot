import logging

from openai import AsyncOpenAI
from config.config import settings

logger = logging.getLogger("call_assessment_bot")

class CallAnalyzer:
    def __init__(self):
        """
        Инициализирует асинхронный клиент для работы через OpenRouter.
        Это решает проблему с гео-блокировками OpenAI.
        """
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            
            api_key=settings.OPENROUTER_API_KEY.get_secret_value(),
            
            default_headers={
                "HTTP-Referer": "https://github.com/crissyro/Call-rating-AI-bot", 
                "X-Title": "Call rating AI bot",
            },
        )
        logger.info("Async client for OpenRouter initialized successfully.")

    async def analyze_call(self, transcript: str) -> str:
        """
        Анализирует расшифровку звонка, используя модели, доступные через OpenRouter.
        """
        system_prompt = (
            "Ты — опытный ИИ-аналитик колл-центра. Твоя задача — анализировать расшифровки "
            "телефонных разговоров. Внимательно изучи предоставленный диалог. "
            "Твой ответ должен быть четким, структурированным и на русском языке. "
            "Предоставь ответ СТРОГО в следующем формате Markdown, без лишних вступлений и заключений:\n\n"
            "**Тональность:** [здесь одно слово: Позитивная, Нейтральная или Негативная]\n\n"
            "**Рекомендации:**\n"
            "1. [здесь первая краткая и конкретная рекомендация по улучшению диалога]\n"
            "2. [здесь вторая краткая и конкретная рекомендация]"
        )
        
        try:
            response = await self.client.chat.completions.create(
                model="google/gemini-flash-1.5",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript}
                ],
                temperature=0.4,
                max_tokens=500,
                timeout=40.0,
            )
            
            result_text = response.choices[0].message.content.strip()
            logger.info(f"Successfully received analysis from OpenRouter. Result length: {len(result_text)}")
            
            return result_text
        
        except Exception as e:
            logger.error(f"An error occurred during OpenRouter API call: {e}", exc_info=True)
            return ("⚠️ **Ошибка анализа**\n\n"
                    "Не удалось связаться с аналитическим сервисом. Пожалуйста, попробуйте снова.")

analyzer = CallAnalyzer()