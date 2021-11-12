'''Клиентская часть'''
import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import time
from decorators import log
from errors import ReqFieldMissingError, IncorrectDataRecivedError, NonDictInputError
from common.metods import send_message, get_message, validate_ip
from common.constants import RESPONSE, ERROR, DEFAULT_LISTEN_ADDR, DEFAULT_LISTEN_PORT, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, STATUS, ONLINE
from logging import getLogger
import logs.client_log_settings

# Подключаем клиентский логгер из client_log_settings
CLIENT_LOGGER = getLogger('client')


@log
def make_presence(account_name='Guest'):
    '''Функция формирования сообщения клиента (словарь), которое он
    отправляет серверу при подключении к нему'''
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            STATUS: ONLINE
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение от пользователя {account_name}')
    return message


@log
def process_ans(message):
    '''Функция обработки ответа от сервера'''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


@log
def connect(host, port):
    '''Функция подключения клиента к серверу с параметрами (host, port)'''
    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect((host, port))
    return client_sock


def main():
    '''Обрабатываем параметры, введенные в консоли'''
    try:
        server_address = sys.argv[1]
        if not validate_ip(server_address):
            CLIENT_LOGGER.critical('IP-адрес сервера задан неверно')
            sys.exit(1)
        server_port = sys.argv[2]
        if not server_port.isdigit():
            CLIENT_LOGGER.critical('Порт должен задаваться числом')
            sys.exit(1)
        server_port = int(server_port)
        if server_port < 1024 or server_port > 65535:
            CLIENT_LOGGER.critical('Порт - число в диапазоне от 1024 до 65535')
            sys.exit(1)
        CLIENT_LOGGER.debug(f'Будет произведено подключение к {server_address}: {server_port}')
    except IndexError:
        CLIENT_LOGGER.error('Неправильные параметры, будет произведено '
              f'подключение к {DEFAULT_LISTEN_ADDR}: {DEFAULT_LISTEN_PORT}')
        server_address = DEFAULT_LISTEN_ADDR
        server_port = DEFAULT_LISTEN_PORT

    # Инициализация сокета и обмен
    try:
        client_sock = connect(server_address, server_port)
    except ConnectionRefusedError:
        # Если сервер ждет соединения от клиента с другим ip адресом (-p 'адрес'), то ошибка
        CLIENT_LOGGER.critical(f'Соединение не установлено, так как сервер {server_address}:{server_port}'
                               ' отверг запрос на подключение')
        sys.exit(1)
    # Отправка сообщения серверу о подключении
    server_name = client_sock.getpeername()
    host_name = client_sock.getsockname()
    CLIENT_LOGGER.debug(f'Подключение клиента {host_name} к серверу {server_name} произведено успешно')
    send_message(make_presence(), client_sock)
    CLIENT_LOGGER.debug(f'Отправлено presence сообщение клиентом {host_name} серверу {server_name}')

    try:
        CLIENT_LOGGER.debug(f'Получен ответ от сервера {server_name}: {process_ans(get_message(client_sock))}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.critical(f'Не удалось декодировать сообщение сервера {server_name}')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except NonDictInputError as input_error:
        CLIENT_LOGGER.error(f'{input_error}')
    except IncorrectDataRecivedError as data_error:
        CLIENT_LOGGER.error(f'{data_error}')

    client_sock.close()
    CLIENT_LOGGER.debug(f'Клиент {host_name} отключен от сервера {server_name}')


if __name__ == '__main__':
    main()
