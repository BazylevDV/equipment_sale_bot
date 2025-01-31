import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
from email.header import Header
import aiosmtplib
from dotenv import load_dotenv  # Для загрузки переменных окружения




# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='a',  # Используем 'a' для добавления в файл, а не перезаписи
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Указываем кодировку UTF-8
)
logger = logging.getLogger(__name__)

# Функция для отправки письма
async def send_email(recipient, subject, body, file_type=None):
    """
    Отправляет email на указанный адрес.

    :param recipient: Адрес получателя.
    :param subject: Тема письма.
    :param body: Текст письма.
    :param file_type: Тип файла для вложения (опционально).
    """
    try:
        # Настройки SMTP сервера
        smtp_server = os.getenv("SMTP_SERVER")  # Сервер SMTP
        smtp_port = int(os.getenv("SMTP_PORT"))  # Порт SMTP
        smtp_username = os.getenv("SMTP_USERNAME")  # Ваш email
        smtp_password = os.getenv("SMTP_PASSWORD")  # Пароль приложения

        if not smtp_username or not smtp_password:
            logger.error("Не указаны SMTP_USERNAME или SMTP_PASSWORD в переменных окружения.")
            return

        # Создание сообщения
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Паритет', smtp_username))
        msg['To'] = formataddr(('Получатель', recipient))
        msg['Subject'] = Header(subject, 'utf-8').encode()  # Убедитесь, что тема кодируется в UTF-8
        msg.set_charset('utf-8')  # Установка кодировки UTF-8

        # Добавление тела письма
        msg.attach(MIMEText(body, 'plain', 'utf-8'))  # Установка кодировки UTF-8 для тела письма

        # Отправка письма
        logger.info(f"Отправка письма на {recipient} с темой: {subject}")
        await aiosmtplib.send(
            msg,
            hostname=smtp_server,
            port=smtp_port,
            username=smtp_username,
            password=smtp_password,
            start_tls=True
        )
        logger.info(f"Письмо успешно отправлено на {recipient}")
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}")
        raise  # Пробрасываем исключение для обработки в вызывающем коде