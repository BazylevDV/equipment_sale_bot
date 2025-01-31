import sys
import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from dotenv import load_dotenv
# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Импортируем обработчики
from app.handlers.handlers import setup_handlers
from app.handlers.request_kp_handlers import setup_request_kp_handlers
from app.handlers.admin import setup_admin_handlers
from db import create_connection, create_table, add_blocked_column
# Загружаем переменные окружения из .env файла
load_dotenv()
# Настройка логирования
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file = 'app.log'
# Настройка логгера для записи в файл с указанием кодировки
my_handler = RotatingFileHandler(filename=log_file, mode="a", maxBytes=5 * 1024 * 1024, backupCount=2, encoding='utf-8', delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
# Настройка консольного вывода
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)
# Создаем глобальный логгер
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)
app_log.addHandler(console_handler)
logger = logging.getLogger('root')

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="admin", description="Admin panel"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    # Создаем соединение с базой данных и создаем таблицу, если она еще не существует
    database = os.path.abspath("database.db")  # абсолютный путь
    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
        add_blocked_column(conn)  # Добавляем столбец blocked, если он еще не существует
    else:
        logger.error("Ошибка! Невозможно создать соединение с базой данных.")
    setup_handlers(dp)
    setup_request_kp_handlers(dp)  # Передаем dp в функцию
    setup_admin_handlers(dp)
    logger.info("Бот включен")
    await set_commands(bot)
    await dp.start_polling(bot)
    logger.info("Бот успешно подключен к серверам Telegram")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Бот выключен')