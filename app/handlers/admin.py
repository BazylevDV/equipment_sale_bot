import logging
import os
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb
from db import create_connection, get_all_requests, block_user, unblock_user

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Admin(StatesGroup):
    block_user = State()
    unblock_user = State()
    broadcast = State()


def setup_admin_handlers(dp: Dispatcher):
    @dp.message(Command("admin"))
    async def admin_panel(message: types.Message):
        # Проверка на администратора
        if message.from_user.id == int(os.getenv("ADMIN_CHAT_ID")):
            await message.answer("Админ-панель", reply_markup=kb.admin_keyboard())
        else:
            await message.answer("У вас нет доступа к админ-панели.")

    @dp.message(Command("get_chat_id"))
    async def get_chat_id(message: types.Message):
        # Проверка на администратора
        if message.from_user.id == int(os.getenv("ADMIN_CHAT_ID")):
            await message.answer(f"Ваш chat_id: {message.chat.id}")
        else:
            await message.answer("У вас нет доступа к этой команде.")

    @dp.callback_query(F.data == "users")
    async def show_users(callback_query: types.CallbackQuery):
        await callback_query.answer()
        conn = create_connection("database.db")
        if conn is not None:
            users = get_all_requests(conn)
            if users:
                user_list = "\n".join(
                    [f"ID: {user[0]}, Организация: {user[1]}, Email: {user[2]}, Телефон: {user[3]}" for user in users])
                await callback_query.message.answer(f"Список пользователей:\n{user_list}")
            else:
                await callback_query.message.answer("Нет пользователей.")
        else:
            await callback_query.message.answer("Ошибка подключения к базе данных.")

    @dp.callback_query(F.data == "stats")
    async def show_stats(callback_query: types.CallbackQuery):
        await callback_query.answer()
        conn = create_connection("database.db")
        if conn is not None:
            users = get_all_requests(conn)
            user_count = len(users)
            await callback_query.message.answer(f"Статистика:\nКоличество пользователей: {user_count}")
        else:
            await callback_query.message.answer("Ошибка подключения к базе данных.")

    @dp.callback_query(F.data == "block")
    async def block_user_start(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.answer()
        await state.set_state(Admin.block_user)
        await callback_query.message.answer("Введите ID пользователя для блокировки:")

    @dp.message(Admin.block_user)
    async def block_user_process(message: types.Message, state: FSMContext):
        user_id = message.text
        conn = create_connection("database.db")
        if conn is not None:
            block_user(conn, user_id)
            await message.answer(f"Пользователь с ID {user_id} заблокирован.")
        else:
            await message.answer("Ошибка подключения к базе данных.")
        await state.finish()

    @dp.callback_query(F.data == "unblock")
    async def unblock_user_start(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.answer()
        await state.set_state(Admin.unblock_user)
        await callback_query.message.answer("Введите ID пользователя для разблокировки:")

    @dp.message(Admin.unblock_user)
    async def unblock_user_process(message: types.Message, state: FSMContext):
        user_id = message.text
        conn = create_connection("database.db")
        if conn is not None:
            unblock_user(conn, user_id)
            await message.answer(f"Пользователь с ID {user_id} разблокирован.")
        else:
            await message.answer("Ошибка подключения к базе данных.")
        await state.finish()

    @dp.callback_query(F.data == "broadcast")
    async def broadcast_start(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.answer()
        await state.set_state(Admin.broadcast)
        await callback_query.message.answer("Отправьте файл для рассылки:")

    @dp.message(Admin.broadcast)
    async def broadcast_process(message: types.Message, state: FSMContext):
        if message.document:
            document = message.document
            file_id = document.file_id
            file_name = document.file_name

            conn = create_connection("database.db")
            if conn is not None:
                users = get_all_requests(conn)
                for user in users:
                    user_id = user[0]
                    await message.bot.send_document(chat_id=user_id, document=file_id,
                                                    caption=f"Новое коммерческое предложение: {file_name}")
                await message.answer(f"Файл {file_name} отправлен всем пользователям.")
            else:
                await message.answer("Ошибка подключения к базе данных.")
        else:
            await message.answer("Пожалуйста, отправьте файл для рассылки.")
        await state.clear()
