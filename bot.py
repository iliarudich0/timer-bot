import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

# Ваш токен бота
TOKEN = os.getenv('TOKEN')

# Логирование ошибок
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция для старта бота
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот с таймером для отправки сообщений.')

# Функция для отправки сообщения по расписанию
def send_scheduled_message(context: CallbackContext) -> None:
    chat_id = context.job.context
    message = "Это запланированное сообщение по таймеру ⏰"
    context.bot.send_message(chat_id=chat_id, text=message)

# Команда для установки таймера
def set_timer(update: Update, context: CallbackContext) -> None:
    try:
        # Установить расписание (каждый час)
        context.job_queue.run_repeating(send_scheduled_message, interval=3600, context=update.message.chat_id)
        update.message.reply_text('Таймер запущен! Я буду отправлять сообщения каждый час.')
    except Exception as e:
        update.message.reply_text(f'Произошла ошибка: {e}')

# Основная функция для запуска бота
def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Команды бота
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('set_timer', set_timer))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
