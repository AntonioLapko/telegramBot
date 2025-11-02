# Для Windows python -m venv env
# env\Scripts\Activate.ps1

#docker build -t lapin_telegram_bot .
#docker images
#docker run lapin_telegram_bot
#docker build . -t cr.yandex/crp3cq2680bsrvs24748/lapin_telegram_bot:latest
#docker push cr.yandex/crp3cq2680bsrvs24748/lapin_telegram_bot:latest




#Настройка SSH
#Шаг 1. Сгенерируйте SSH‑ключ (если нет): ssh-keygen -t ed25519 -C "ваш_email@example.com"
#Шаг 2. Добавьте ключ в SSH‑агент: eval "$(ssh-agent -s)"
#ssh-add ~/.ssh/id_ed25519

#Шаг 3. Добавьте публичный ключ в GitHub: Откройте файл ~/.ssh/id_ed25519.pub и скопируйте его содержимое.
#Шаг 4. Переключите URL репозитория на SSH: git remote set-url origin git@github.com:AntonioLapko/telegramBot.git

#Проверьте URL репозитория git remote -v


import logging
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
)
import asyncio

# Ваш токен от @BotFather
TOKEN = "8482269363:AAEetzUmFKJGhgx9lCFBQHQptb-LMMJxbZ0"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),  # Лог в файл
        logging.StreamHandler(),  # Лог в консоль
    ],
)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI()

# Глобальная переменная для доступа к боту из FastAPI
bot_app: Application | None = None


# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.message.chat_id

    welcome_text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я простой бот, который отвечает на любые сообщения фразой «И чё?».\n"
        "Попробуй написать что‑нибудь!"
    )

    logger.info(f"Пользователь {user.full_name} (ID: {user.id}) запустил бота (/start)")
    await update.message.reply_text(welcome_text)


# Функция-обработчик сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    chat_id = update.message.chat_id

    logger.info(
        f"Получено сообщение от пользователя {user.full_name} (ID: {user.id}, "
        f"чат: {chat_id}): \"{message_text}\""
    )

    response_text = "И чё?"
    await update.message.reply_text(response_text)

    logger.info(f"Отправлен ответ в чат {chat_id}: \"{response_text}\"")

# HTTP-эндпоинт POST /hello
@app.post("/hello")
async def hello_endpoint(request: Request) -> JSONResponse:
    try:
        # Получаем тело запроса как JSON
        body: Dict[str, Any] = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Неверный JSON в теле запроса")

    # Формируем ответ
    response_data = {"response": "hello"}

    logger.info(f"Обработан POST /hello. Тело запроса: {body}")

    return JSONResponse(content=response_data)

# Функция запуска бота и сервера
async def run_bot_and_server():
    global bot_app

    # Инициализируем Telegram-бота
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Бот запущен и ожидает сообщений...")

    # Запускаем бота в фоне
    await bot_app.start()
    await bot_app.updater.start_polling(
        poll_interval=2.0,
        timeout=20,
        allowed_updates=None,
        drop_pending_updates=False,
    )

    # FastAPI будет запущен в отдельном потоке (см. ниже)

# Точка входа
if __name__ == "__main__":
    import uvicorn

    # Запускаем бот и сервер параллельно
    asyncio.run(run_bot_and_server())

    # Запуск FastAPI (в отдельном потоке, т.к. asyncio.run уже работает)
    uvicorn.run(app, host="0.0.0.0", port=8080)