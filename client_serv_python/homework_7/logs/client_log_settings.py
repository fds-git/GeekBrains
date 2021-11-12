"""Настройки клиентского логгера"""

import sys
import os
import logging
from common.constants import LOGGING_LEVEL
#sys.path.append('../')

# создаём формировщик логов (formatter):
CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Определяем директорию, из которой запускается текущий файл
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, "logs")
# Если в этой директории нет вложенной папки logs, то создаем ее
# Таким образом разделяем файлы настроек и самих логов
if not os.path.exists(PATH):
    os.makedirs(PATH)
PATH = os.path.join(PATH, 'client.log')

# Поток вывода в консоль
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.DEBUG)

# Поток вывода в файл
LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(CLIENT_FORMATTER)
LOG_FILE.setLevel(logging.DEBUG)

# Создаём регистратор и настраиваем его
LOGGER = logging.getLogger('client')
#LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
