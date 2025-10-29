# Для Windows python -m venv env
# env\Scripts\Activate.ps1

#docker build -t lapin_telegram_bot .
#docker images
#docker run -p 5000:5000 lapin_telegram_bot
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
from telegram import Update
from telegram.ext import (Application, MessageHandler, filters, ContextTypes, CommandHandler)

# Ваш токен от @BotFather
TOKEN = '8482269363:AAEetzUmFKJGhgx9lCFBQHQptb-LMMJxbZ0'

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),  # Лог в файл
        logging.StreamHandler()  # Лог в консоль
    ]
)
logger = logging.getLogger(__name__)

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.message.chat_id

    # Приветственное сообщение
    welcome_text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я простой бот, который отвечает на любые сообщения фразой «И чё?».\n"
        "Попробуй написать что‑нибудь!"
    )

    # Логируем команду /start
    logger.info(f'Пользователь {user.full_name} (ID: {user.id}) запустил бота (/start)')

    # Отправляем приветствие
    await update.message.reply_text(welcome_text)
# Функция-обработчик сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    chat_id = update.message.chat_id

    # Логируем входящее сообщение
    logger.info(
        f'Получено сообщение от пользователя {user.full_name} (ID: {user.id}, '
        f'чат: {chat_id}): "{message_text}"'
    )

    # Отправляем ответ
    response_text = 'И чё?'
    await update.message.reply_text(response_text)

    # Логируем отправленный ответ
    logger.info(
        f'Отправлен ответ в чат {chat_id}: "{response_text}"'
    )

def main():
    # Создаём приложение и передаём токен
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))  # /start
    # Добавляем обработчик любых текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    logger.info('Бот запущен и ожидает сообщений...')
    application.run_polling()

if __name__ == '__main__':
    main()
