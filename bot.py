import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler


# Загрузить переменные из .env файла
load_dotenv()

# Получить токен из переменной окружения
TOKEN = os.getenv('TOKEN')

# Логирование ошибок
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция для старта бота
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот с таймером для отправки сообщений.')

# Функция для отправки сообщения по расписанию
async def send_scheduled_message(context: CallbackContext) -> None:
    chat_id = context.job.context
    message = "Это запланированное сообщение по таймеру ⏰"
    await context.bot.send_message(chat_id=chat_id, text=message)

# Команда для установки таймера
async def set_timer(update: Update, context: CallbackContext) -> None:
    try:
        # Установить расписание (каждый час)
        context.job_queue.run_repeating(send_scheduled_message, interval=3600, context=update.message.chat_id)
        await update.message.reply_text('Таймер запущен! Я буду отправлять сообщения каждый час.')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {e}')

# Основная функция для запуска бота
async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Команды бота
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('set_timer', set_timer))

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
