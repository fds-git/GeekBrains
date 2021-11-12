"""Клиентская часть"""
import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import time
import argparse
from logging import getLogger
from decorators import log
import threading
from errors import ReqFieldMissingError, IncorrectDataRecivedError, NonDictInputError, ServerError
from common.metods import send_message, get_message, validate_ip
from common.constants import RESPONSE, ERROR, DEFAULT_LISTEN_ADDR, DEFAULT_LISTEN_PORT, \
    ACTION, PRESENCE, TIME, SOURCE, MESSAGE_TEXT, MESSAGE, DESTINATION, EXIT

import logs.client_log_settings

# Подключаем клиентский логгер из client_log_settings
CLIENT_LOGGER = getLogger('client')


@log
def message_receiver(client_socket, this_user):
    """Функция - обработчик сообщений других клиентов, поступающих через сервер.
    Выводит полученное сообщение в консоль"""
    while True:
        try:
            message = get_message(client_socket)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SOURCE in message and MESSAGE_TEXT in message and DESTINATION in message \
                    and message[DESTINATION] == this_user:
                print(f'\nСообщение от пользователя {message[SOURCE]}: {message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Сообщение от пользователя {message[SOURCE]}: {message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение от сервера: {message}')
        except IncorrectDataRecivedError:
            CLIENT_LOGGER.error(f'Не удалось декодировать сообщение')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Потеряно соединение с сервером')
            break


@log
def create_message(source, destination, message):
    """Функция формирования словаря с сообщением пользователя"""
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        SOURCE: source,
        DESTINATION: destination,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def create_exit_message(account_name):
    """Функция создания сообщения о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        SOURCE: account_name
    }


@log
def create_presence_message(account_name):
    """Функция формирования сообщения клиента (словарь), которое он
    отправляет серверу при подключении к нему"""
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        SOURCE: account_name,
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение от пользователя {account_name}')
    return message


@log
def process_server_answer(message):
    """Функция обработки ответа от сервера после попытки клиента подключиться"""
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
def message_sender(client_socket, source):
    """Функция взаимодействия с пользователем, запрашивает данные, отправляет сообщения"""
    print(f'Имя данного клиента: {source}')
    print('Список команд:')
    print('message - отправить сообщение')
    print('exit - выход')
    while True:

        action = input(f'Введите действие: ')
        if action == 'message':
            destination = input(f'Введите имя получателя: ')
            message = input(f'Введите сообщение для {destination}: ')
            send_message(create_message(source, destination, message), client_socket)
        elif action == 'exit':
            send_message(create_exit_message(source), client_socket)
            print('Отключение клиента')
            CLIENT_LOGGER.info('Пользователь завершил работу клиента')
            time.sleep(1)
            break
        else:
            print('Список возможных команд:')
            print('message - отправить сообщение;')
            print('exit - выход из программы.')


@log
def arg_parser():
    """Обработка аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_LISTEN_ADDR, nargs='?')
    parser.add_argument('-p', default=DEFAULT_LISTEN_PORT, type=int, nargs='?')
    parser.add_argument('-n', default='none', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p
    client_name = namespace.n

    # Проверка принадлежит ли номер порта возможному диапазону
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical('Возможные номера портов от 1024 до 65535')
        sys.exit(1)

    # Проверка правильности IP-адреса
    if not validate_ip(server_address):
        CLIENT_LOGGER.critical('IP-адрес сервера задан неверно')
        sys.exit(1)

    return server_address, server_port, client_name


@log
def connect(host, port):
    """Функция подключения клиента к серверу с параметрами (host, port)"""
    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect((host, port))
    return client_sock


def main():
    """Подключаемся к серверу и принимаем или отправляем сообщения в зависимости от режима работы"""
    server_address, server_port, client_name = arg_parser()

    CLIENT_LOGGER.info(
        f'Попытка подключения к серверу: {server_address} через порт: {server_port}')

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
    send_message(create_presence_message(client_name), client_sock)
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
        # Если соединение с сервером установлено, то запускаем клиентский поток приёма сообщний
        receiver = threading.Thread(target=message_receiver, args=(client_sock, client_name))
        receiver.daemon = True
        receiver.start()

        # Запускаем клиентский поток отправки сообщений и взаимодействия с пользователем
        sender = threading.Thread(target=message_sender, args=(client_sock, client_name))
        sender.daemon = True
        sender.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        # В процессе работают два потока (в одной консоли):
        # на прием сообщений и отправку сообщений. Выход из
        # цикла по команде пользователя или при ошибке
        while True:
            time.sleep(2)
            if receiver.is_alive() and sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
