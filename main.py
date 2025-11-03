# Для Windows python -m venv env
# env\Scripts\Activate.ps1

#docker build -t lapin_telegram_bot .
#docker images
#docker run lapin_telegram_bot
#docker build . -t cr.yandex/crplo5125gv8esvpt42k/lapin_telegram_bot:1.1.0
#docker push cr.yandex/crplo5125gv8esvpt42k/lapin_telegram_bot:1.1.0
#docker tag 9f3a31473d6a cr.yandex/crplo5125gv8esvpt42k/lapin_telegram_bot:1.0.2

#TOKEN = "8482269363:AAEetzUmFKJGhgx9lCFBQHQptb-LMMJxbZ0"
#curl -X POST "https://api.telegram.org/bot8482269363:AAEetzUmFKJGhgx9lCFBQHQptb-LMMJxbZ0/setWebhook" \
#     -d 'url=https://d5dgn53kgfesereq4a0j.zj2i1qoy.apigw.yandexcloud.net/bot'



#Настройка SSH
#Шаг 1. Сгенерируйте SSH‑ключ (если нет): ssh-keygen -t ed25519 -C "ваш_email@example.com"
#Шаг 2. Добавьте ключ в SSH‑агент: eval "$(ssh-agent -s)"
#ssh-add ~/.ssh/id_ed25519

#Шаг 3. Добавьте публичный ключ в GitHub: Откройте файл ~/.ssh/id_ed25519.pub и скопируйте его содержимое.
#Шаг 4. Переключите URL репозитория на SSH: git remote set-url origin git@github.com:AntonioLapko/telegramBot.git

#Проверьте URL репозитория git remote -v

from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8482269363:AAEetzUmFKJGhgx9lCFBQHQptb-LMMJxbZ0"
application = None
http_server = None

def get_main_menu():
    keyboard = [
        [KeyboardButton("ТО авто")],
        [KeyboardButton("Коммуналка")],
        [KeyboardButton("Расходы")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Здравствуйте!\n\n"
        "Я ваш персональный помощник. Выберите действие из меню ниже:"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu())

async def echo_icho(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("И чё?")


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "ТО авто":
        response = "Вы выбрали раздел «ТО авто». Здесь можно:\n- Записать на ТО\n- Проверить историю обслуживания\n- Рассчитать стоимость работ"
    elif text == "Коммуналка":
        response = "Вы выбрали раздел «Коммуналка». Здесь можно:\n- Оплатить услуги\n- Посмотреть историю платежей\n- Получить квитанцию"
    elif text == "Расходы":
        response = "Вы выбрали раздел «Расходы». Здесь можно:\n- Добавить новую трату\n- Просмотреть статистику\n- Установить бюджет"
    else:
        response = "И чё?"

    await update.message.reply_text(response, reply_markup=get_main_menu())

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/bot':
            self.send_error(404, "Not Found")
            return

        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            # Получаем loop из глобального контекста
            loop = asyncio.get_event_loop()
            # Планируем задачу в loop
            asyncio.run_coroutine_threadsafe(
                application.update_queue.put(Update.de_json(data)),
                loop
            )

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

        except json.JSONDecodeError:
            logger.error("Невалидный JSON в запросе")
            self.send_error(400, "Bad Request: Invalid JSON")
        except Exception as e:
            logger.error(f"Ошибка обработки запроса: {e}")
            self.send_error(500, "Internal Server Error")


def main():
    global application, http_server
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex('^/(?!start)'), echo_icho))

    # Запускаем приложение Telegram в фоне

    application.run_webhook(
        listen='0.0.0.0',
        port=8080,
        url_path='/bot',
        webhook_url='https://d5dgn53kgfesereq4a0j.zj2i1qoy.apigw.yandexcloud.net/bot'
    )

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Сервер остановлен")
    finally:
        http_server.server_close()


if __name__ == '__main__':
    main()