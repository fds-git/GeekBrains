'''Описание констант проекта'''

from logging import DEBUG
RESPONDEFAULT_IP_ADDRESSSE = 'respondefault_ip_addressse'
ERROR = 'error'
# Порт для прослушки по умолчанию
DEFAULT_LISTEN_PORT = 7777
# Адрес для прослушки по умолчанию
DEFAULT_LISTEN_ADDR = '127.0.0.1'
# Максимальное количество подключений в очереди
MAX_CONNECTIONS = 7

RESPONSE = 'response'

ACTION = 'action'
PRESENCE = 'presence'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
STATUS = 'status'
ONLINE = 'online'
PROBE = 'probe'
# Кодировка
ENCODING = 'utf-8'
# Максимальная длина сообщения
MAX_LENGTH = 1024
# Текущий уровень логирования
LOGGING_LEVEL = DEBUG
SENDER = 'sender'
MESSAGE_TEXT = 'message_text'
MESSAGE = 'message'
# Интервал, через котороый сервер будет проверять, хочет ли кто к нему подключиться
TIMEOUT = 0.5
