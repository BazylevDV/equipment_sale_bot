import logging

# Настройка логгера
logging.basicConfig(
    filename='app.log',  # Имя файла, куда будут записываться логи
    level=logging.INFO,  # Уровень логирования (INFO, WARNING, ERROR и т.д.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи логов
)

# Запись простого сообщения в лог
logging.info("Проверка логгера")
subject = "Привет, это тема письма!"
logging.info(f"Тема письма: {subject}")