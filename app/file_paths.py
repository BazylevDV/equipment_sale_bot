import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Определение корневой директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Пути к файлам
FILE_PATHS = {
    "catalog": os.path.join(BASE_DIR, "app", "files", "catalog", "Паритет_Диагностическое оборудование_2023 (2).pdf"),
    "warehouse": os.path.join(BASE_DIR, "app", "files", "stock", "Паритет _Спец и Склад _Q1.25.pdf"),
    "promo1": os.path.join(BASE_DIR, "app", "files", "promo", "Копия КП_Спец предложение__GE Versana Active_2024-09-30.xls"),
    "promo2": os.path.join(BASE_DIR, "app", "files", "promo", "Паритет _Спец и Склад _Q1.25.doc"),
}

# MIME-типы файлов
MIME_TYPES = {
    "catalog": 'application/pdf',
    "warehouse": 'application/pdf',
    "promo1": 'application/vnd.ms-excel',  # xls
    "promo2": 'application/msword',        # doc
}

# Проверка существования файлов
def check_file_paths():
    for file_type, file_path in FILE_PATHS.items():
        logger.info(f"Проверка пути к файлу: {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден: {file_path}")
            raise FileNotFoundError(f"Файл не найден: {file_path}")

# Функция для получения MIME-типа
def get_mime_type(file_type):
    return MIME_TYPES.get(file_type, 'application/octet-stream')