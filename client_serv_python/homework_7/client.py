'''Клиентская часть'''
import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import time
import argparse
from logging import getLogger
from decorators import log
from errors import ReqFieldMissingError, IncorrectDataRecivedError, NonDictInputError, ServerError
from common.metods import send_message, get_message, validate_ip
from common.constants import RESPONSE, ERROR, DEFAULT_LISTEN_ADDR, DEFAULT_LISTEN_PORT, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, SENDER, MESSAGE_TEXT, MESSAGE

import logs.client_log_settings

# Подключаем клиентский логгер из client_log_settings
CLIENT_LOGGER = getLogger('client')


@log
def print_message(message):
    """Функция выводит в консоль сообщения, отправленные другими пользователями"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение от сервера: {message}')


@log
def create_message(client_sock, account_name='Guest'):
    """Функция для ввода текста сообщения пользователем"""
    message = input('Введите сообщение или \'exit\' для выхода: ')
    if message == 'exit':
        client_sock.close()
        CLIENT_LOGGER.info('Произведен выход из программы')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def create_presence_message(account_name='Guest'):
    '''Функция формирования сообщения клиента (словарь), которое он
    отправляет серверу при подключении к нему'''
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение от пользователя {account_name}')
    return message


@log
def process_server_answer(message):
    '''Функция обработки ответа от сервера'''
    CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
        else:
            raise IncorrectDataRecivedError
    raise ReqFieldMissingError(RESPONSE)


@log
def arg_parser():
    """Обработка аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_LISTEN_ADDR, nargs='?')
    parser.add_argument('-p', default=DEFAULT_LISTEN_PORT, type=int, nargs='?')
    parser.add_argument('-m', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p
    client_mode = namespace.m

    # Проверка принадлежит ли номер порта возможному диапазону
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical('Возможные номера портов от 1024 до 65535')
        sys.exit(1)

    # Проверка правильности режима работы клиента
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                               f'допустимые режимы: listen , send')
        sys.exit(1)

    # Проверка правильности IP-адреса
    if not validate_ip(server_address):
        CLIENT_LOGGER.critical('IP-адрес сервера задан неверно')
        sys.exit(1)

    return server_address, server_port, client_mode


@log
def connect(host, port):
    '''Функция подключения клиента к серверу с параметрами (host, port)'''
    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect((host, port))
    return client_sock


def main():
    '''Подключаемся к серверу и принимаем или отправляем сообщения в зависимости от режима работы'''
    server_address, server_port, client_mode = arg_parser()

    CLIENT_LOGGER.info(
        f'Будет запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, режим работы: {client_mode}')

    # Попытка подключения к серверу
    try:
        client_sock = connect(server_address, server_port)
    except ConnectionRefusedError:
        # Если сервер ждет соединения от клиента с другим ip адресом (-p 'адрес'), то ошибка
        CLIENT_LOGGER.critical(f'Соединение не установлено, так как сервер '
                               f'{server_address}:{server_port} отверг запрос на подключение')
        sys.exit(1)

    # Отправка сообщения серверу о подключении
    server_name = client_sock.getpeername()
    host_name = client_sock.getsockname()
    CLIENT_LOGGER.debug(f'Подключение клиента {host_name} к серверу {server_name} '
                        f'произведено успешно')
    send_message(create_presence_message(), client_sock)
    CLIENT_LOGGER.debug(f'Отправлено presence сообщение клиентом {host_name} серверу {server_name}')

    try:
        CLIENT_LOGGER.debug(f'Получен ответ от сервера {server_name}: '
                            f'{process_server_answer(get_message(client_sock))}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.critical(f'Не удалось декодировать сообщение сервера {server_name}')
        CLIENT_LOGGER.debug(f'Клиент {host_name} отключен от сервера {server_name}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
        CLIENT_LOGGER.debug(f'Клиент {host_name} отключен от сервера {server_name}')
        sys.exit(1)
    except NonDictInputError as input_error:
        CLIENT_LOGGER.error(f'{input_error}')
        CLIENT_LOGGER.debug(f'Клиент {host_name} отключен от сервера {server_name}')
        sys.exit(1)
    except IncorrectDataRecivedError as data_error:
        CLIENT_LOGGER.error(f'{data_error}')
        CLIENT_LOGGER.debug(f'Клиент {host_name} отключен от сервера {server_name}')
        sys.exit(1)

    else:
        # Если соединение с сервером установлено корректно,
        # то отправляем или принимаем сообщения от него в
        # зависимости от режима работы клиента
        if client_mode == 'send':
            print('Режим работы клиента - отправка сообщений')
        else:
            print('Режим работы клиента - приём сообщений')
        while True:
            # Если режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(create_message(client_sock), client_sock)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно')
                    sys.exit(1)

            # Если режим работы - приём сообщений:
            if client_mode == 'listen':
                try:
                    # Будет висеть в get_message, пока не получит сообщение
                    print_message(get_message(client_sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно')
                    sys.exit(1)


if __name__ == '__main__':
    main()
