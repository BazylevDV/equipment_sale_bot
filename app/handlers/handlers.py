from aiogram import Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramAPIError
import asyncio
from app.file_paths import FILE_PATHS, MIME_TYPES  # Импортируем переменные
import os  # Импортируем os для работы с переменными окружения
from db import create_connection, create_request, check_unique_request  # Импортируем функции для работы с базой данных
import logging

# Используем глобальный логгер
logger = logging.getLogger('root')


class EmailRequest(StatesGroup):
    email = State()


async def send_welcome_message(message: types.Message, state: FSMContext):
    await message.answer(
        "Здравствуйте! 👋 Приветствуем Вас в нашем чат-боте отдела медицинского оборудования. Если Вам нужно приобрести медицинское оборудование по принципу 'Здесь и сейчас', то Вам сюда:")
    main_menu = kb.get_main_menu()
    await message.answer('Внизу выберите нужный пункт в меню. ✨', reply_markup=main_menu)


def setup_handlers(dp: Dispatcher):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message, state: FSMContext):
        # Отправляем приветственное сообщение и клавиатуру
        logger.info(f"Пользователь {message.from_user.id} начал взаимодействие с ботом")
        await send_welcome_message(message, state)

    @dp.message(F.text == "Каталог оборудования 🗂️")
    async def catalog_handler(message: types.Message):
        file_path = FILE_PATHS.get("catalog")  # Получаем путь к файлу каталога
        if file_path:
            file = FSInputFile(file_path)  # Создаем объект файла
            await message.answer_document(file)  # Отправляем файл в чат
            await message.answer("Вот ваш каталог оборудования! 🗂️")
        else:
            await message.answer("Файл каталога не найден. Пожалуйста, свяжитесь с администратором.")
        logger.info(f"Пользователь {message.from_user.id} запросил каталог оборудования")

    @dp.message(F.text == "Склад на сегодня 🏬")
    async def warehouse_handler(message: types.Message):
        file_path = FILE_PATHS.get("warehouse")  # Получаем путь к файлу склада
        if file_path:
            file = FSInputFile(file_path)  # Создаем объект файла
            await message.answer_document(file)  # Отправляем файл в чат
            await message.answer("Вот информация о складе на сегодня! 🏬")
        else:
            await message.answer("Файл склада не найден. Пожалуйста, свяжитесь с администратором.")
        logger.info(f"Пользователь {message.from_user.id} запросил информацию о складе на сегодня")

    @dp.message(F.text == "Успей купить по акции-1 ☎️")
    async def promo_handler_1(message: types.Message):
        file_path = FILE_PATHS.get("promo1")  # Получаем путь к файлу акции-1
        if file_path:
            file = FSInputFile(file_path)  # Создаем объект файла
            await message.answer_document(file)  # Отправляем файл в чат
            await message.answer("Вот информация по акции-1! ☎️")
        else:
            await message.answer("Файл акции-1 не найден. Пожалуйста, свяжитесь с администратором.")
        logger.info(f"Пользователь {message.from_user.id} запросил информацию по акции-1")

    @dp.message(F.text == "Успей купить по акции-2 ☎️")
    async def promo_handler_2(message: types.Message):
        file_path = FILE_PATHS.get("promo2")  # Получаем путь к файлу акции-2
        if file_path:
            file = FSInputFile(file_path)  # Создаем объект файла
            await message.answer_document(file)  # Отправляем файл в чат
            await message.answer("Вот информация по акции-2! ☎️")
        else:
            await message.answer("Файл акции-2 не найден. Пожалуйста, свяжитесь с администратором.")
        logger.info(f"Пользователь {message.from_user.id} запросил информацию по акции-2")

    @dp.message(F.text == "О нас 📝")
    async def info_handler(message: types.Message):
        info_text = (
            "👋 *Добро пожаловать в бот отдела мед.оборудования челябинского филиала группы 'Паритет'!* 🏥\n\n"
            "📝 *Информация о компании:* \n"
            " Мы ценим Ваше время и деньги и готовы помочь Вам с выбором необходимого оборудования и ответить на все Ваши вопросы.\n\n"
            "📞 *Контактные данные:* \n"
            "- 🏙️ Челябинск, ООО 'Паритет-Челябинск' ул. Постышева д.2 офис 204, 101\n"
            "- 📞 Городские номера:\n"
            "   - +7-351-274-40-17\n"
            "   - +7-351-274-40-19\n"
            "- 🔢 Внутренние номера:\n"
            "   - 120\n"
            "   - 121\n"
            "   - 107\n\n"
            "📧 *Заявки на лицензированный ремонт и сервис направлять сюда: @ParitetReceptionBot* \n"
            "Вы можете отправить через бот запрос на КП наш адрес электронной почты, и мы свяжемся с Вами в ближайшее время!\n\n"
            "⚠️ *Важно:* Информация от бота меняется по наличию, номенклатуре и ценам , поэтому не  является офертой, уточняйте у менеджеров напрямую."
        )
        await message.answer(info_text, parse_mode="Markdown")
        logger.info(f"Пользователь {message.from_user.id} запросил информацию о компании")

    async def remind_user(message: types.Message, state: FSMContext):
        await asyncio.sleep(60 * 5)  # 5 минут
        data = await state.get_data()
        if data.get("email") is None:
            await message.answer(
                "Вы еще не ввели рабочий адрес электронной почты. Хотите продолжить или завершить сеанс?")
            await message.answer("Выберите действие:", reply_markup=kb.reminder_keyboard())

    @dp.callback_query(F.data == "continue")
    async def continue_session(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.answer()
        await callback_query.message.answer("Продолжаем сеанс. Введите адрес электронной почты:")
        logger.info(f"Пользователь {callback_query.from_user.id} выбрал продолжить сеанс")

    @dp.callback_query(F.data == "finish")
    async def finish_session(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.answer()
        await state.clear()  # Используем clear() вместо finish() в aiogram 3.x
        await callback_query.message.answer("Сеанс завершен. Спасибо за использование бота!",
                                            reply_markup=kb.get_main_menu())
        logger.info(f"Пользователь {callback_query.from_user.id} завершил сеанс")

    @dp.message(StateFilter(EmailRequest.email))
    async def start_reminder(message: types.Message, state: FSMContext):
        asyncio.create_task(remind_user(message, state))
        await asyncio.sleep(0)  # Чтобы избежать предупреждения о не ожидаемой корутине

    @dp.message(Command("admin"))
    async def admin_panel(message: types.Message):
        # Проверка на администратора
        if message.from_user.id == int(os.getenv("ADMIN_CHAT_ID")):
            await message.answer("Админ-панель", reply_markup=kb.admin_keyboard())
        else:
            await message.answer("У вас нет доступа к админ-панели.")
        logger.info(f"Пользователь {message.from_user.id} запросил админ-панель")
