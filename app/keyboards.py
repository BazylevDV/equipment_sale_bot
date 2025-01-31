from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def get_main_menu():
    """
    Создает главное меню с кнопками.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, keyboard=[
        [KeyboardButton(text="Каталог оборудования 🗂️"), KeyboardButton(text="Склад на сегодня 🏬")],
        [KeyboardButton(text="Успей купить по акции-1 ☎️"), KeyboardButton(text="Успей купить по акции-2 ☎️")],
        [KeyboardButton(text="Запросить КП🖊️"), KeyboardButton(text="О нас 📝")]
    ])
    return keyboard


def back_keyboard():
    """
    Создает клавиатуру с кнопкой "Назад".
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад 👈", callback_data="back")]
    ])
    return keyboard


def reminder_keyboard():
    """
    Создает клавиатуру для напоминания.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить ▶️", callback_data="continue")],
        [InlineKeyboardButton(text="Завершить сеанс ⏹️", callback_data="finish")]
    ])
    return keyboard


def manager_keyboard():
    """
    Создает клавиатуру с менеджерами.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дружинина Татьяна 📞", callback_data="Дружинина Татьяна")],
        [InlineKeyboardButton(text="Ковач Александр 📞", callback_data="Ковач Александр")]
    ])
    return keyboard


def restart_keyboard():
    """
    Создает клавиатуру для повторного запуска.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить ▶️", callback_data="continue_kp")],
        [InlineKeyboardButton(text="Начать заново 🔄", callback_data="restart_kp")]
    ])
    return keyboard


def subscribe_keyboard():
    """
    Создает клавиатуру для перехода на бота.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти на бота 👌", url="https://t.me/LabDealsBot")]
    ])
    return keyboard


def admin_keyboard():
    """
    Создает клавиатуру для админ-панели.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пользователи 🧑‍💻", callback_data="users")],
        [InlineKeyboardButton(text="Статистика 📊", callback_data="stats")],
        [InlineKeyboardButton(text="Блокировка 🔐", callback_data="block")],
        [InlineKeyboardButton(text="Разблокировка 🗝️", callback_data="unblock")],
        [InlineKeyboardButton(text="Рассылка 📤", callback_data="broadcast")]
    ])
    return keyboard