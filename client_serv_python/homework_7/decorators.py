"""Декораторы"""

import sys
import logging
#import logs.server_log_settings
#import logs.client_log_settings
import inspect

# Определяем из какого файла был запущен скрипт
# и в соответствии с этим загружаем нужный логгер
if 'client' in sys.argv[0]:
    LOGGER = logging.getLogger('client')
else:
    LOGGER = logging.getLogger('server')


def log(func_to_log):
    """Функция-декоратор"""
    def func_logger(*args, **kwargs):
        result = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Функция {func_to_log.__name__}, описана в файле '
                     f'{inspect.getfile(func_to_log)}, '
                     f'вызвана с параметрами {args}, {kwargs} из функции {inspect.stack()[1][3]}, '
                     f'описанной в файле {inspect.stack()[1][1]}')
        return result
    return func_logger
