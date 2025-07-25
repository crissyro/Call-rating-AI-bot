# 🤖 Call Rating AI Bot

![CI/CD](https://github.com/crissyro/Call-rating-AI-bot/actions/workflows/ci.yml/badge.svg)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)
![Ruff](https://img.shields.io/badge/Linter-Ruff-yellow.svg)
![OpenRouter](https://img.shields.io/badge/OpenRouter-API-lightgrey.svg)
![License](https://img.shields.io/github/license/crissyro/Call-rating-AI-bot)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)

---

ИИ-бот для анализа тональности телефонных звонков и предоставления рекомендаций по улучшению диалога. Работает с расшифровками разговоров, взаимодействует с пользователем через Telegram и использует мощные ИИ-модели через [OpenRouter](https://openrouter.ai).

---

##  Возможности

- Определяет **тональность** диалога: Позитивная / Нейтральная / Негативная.
- Даёт **2 конкретные рекомендации** по улучшению.
- Работает полностью **на русском языке**.
- Устойчив к сбоям: все ошибки логируются и обрабатываются корректно.

---

##  Используемая модель

Модель: [`google/gemini-flash-1.5`](https://openrouter.ai/models/google/gemini-flash-1.5)
Платформа: [OpenRouter](https://openrouter.ai)
Преимущества:
- Высокая скорость генерации
- Совместимость с OpenAI API
- Возможность обхода гео-блокировок

---

## 📦 Установка и запуск

### 1. Клонируйте репозиторий:

```bash
git clone https://github.com/crissyro/Call-rating-AI-bot.git
cd Call-rating-AI-bot
```

### 2. Установите зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

> ✅ Выдайте токен в @BotFather
> 🔑 Получите API-ключ на: https://openrouter.ai/keys

### 4. Запуск бота:

```bash
python3 src/main.py
```

---

## CI / Code Quality

Бот проверяется через GitHub Actions при каждом пуше:

- ✅ **Ruff** — линтинг и проверка форматирования
- ✅ **pre-commit** — автофиксация форматирования и ошибок

Чтобы запускать проверки локально:

```bash
pre-commit install
pre-commit run --all-files
```

---

## Ограничения

- Бот работает **только с текстовыми сообщениями**.
- Минимум **10 слов** в сообщении для запуска анализа.
- Анализ может занимать до **30 секунд**.
- Работает только с **русскими текстами**.

---

## Что можно улучшить

При наличии большего времени и ресурсов:

- Добавить веб-интерфейс с историей и графиками
- Перевод на многоязычную поддержку
- Возможность обучения на пользовательских диалогах
- Хранение и экспорт истории анализов

---

## 👨‍💻 Автор

**Roman Moroz**
[GitHub: @crissyro](https://github.com/crissyro)

---

## 📄 Лицензия

MIT License. См. файл [`LICENSE`](LICENSE) для подробностей.
