"""Настройки серверного логгера"""

import sys
import os
import logging
import logging.handlers
from common.constants import LOGGING_LEVEL
#sys.path.append('../')

# Создаём формировщик логов (formatter):
SERVER_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Определяем директорию, из которой запускается текущий файл
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, "logs")
# Если в этой директории нет вложенной папки logs, то создаем ее
# Таким образом разделяем файлы настроек и самих логов
if not os.path.exists(PATH):
    os.makedirs(PATH)
PATH = os.path.join(PATH, 'server.log')

# Поток вывода в консоль
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.DEBUG)

# Поток вывода в файл
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
#LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(SERVER_FORMATTER)
LOG_FILE.setLevel(logging.DEBUG)

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger('server')
#LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
