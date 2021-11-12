'''Серверная часть'''
import sys
import json
import socket
import argparse
import time
import select
from socket import socket, AF_INET, SOCK_STREAM
from logging import getLogger
from errors import IncorrectDataRecivedError, NonDictInputError
from common.metods import send_message, get_message, validate_ip
from common.constants import ERROR, DEFAULT_LISTEN_PORT, \
    MAX_CONNECTIONS, ACTION, TIME, PRESENCE, USER, ACCOUNT_NAME, \
    RESPONSE, MESSAGE, MESSAGE_TEXT, SENDER, TIMEOUT
from decorators import log
import logs.server_log_settings

# Подключаем серверный логгер из server_log_settings
SERVER_LOGGER = getLogger('server')


@log
def process_client_message(message, messages_list, client):
    """Функция для обработки сообщений клинтов. Проверяет на правильность
    информационное сообщение или сообщение присутствия от клиента.
    Если сообщение сформировано неправильно, отправляет клиенту Bad Request"""

    SERVER_LOGGER.debug(f'Определение типа и правильности сообщения : {message}'
                        'клиента {client.getpeername()}')
    # Если это сообщение о присутствии и оно правильно, то отправляет клиенту RESPONSE: 200
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message({RESPONSE: 200}, client)
        # Если раскомментить, то не будет работать
        #SERVER_LOGGER.debug(f'ОТправлено сообщение {RESPONSE: 200} клиенту {client}')
        return
    # Если это информационное сообщение и оно правильно, то добавляем его в очередь
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    # Иначе отправляем Bad request
    else:
        send_message({
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }, client)
        return


@log
def arg_parser():
    """Обработка аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_LISTEN_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # Проверка принадлежит ли номер порта возможному диапазону
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical('Возможные номера портов от 1024 до 65535')
        sys.exit(1)

    # Проверка правильности IP-адреса
    if not validate_ip(listen_address) and listen_address != '':
        SERVER_LOGGER.critical('IP-адрес сервера задан неверно')
        sys.exit(1)

    return listen_address, listen_port


@log
def launch(listen_address, listen_port, timeout, max_connections):
    """Функция запуска сервера"""
    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.bind((listen_address, listen_port))
    serv_sock.listen(max_connections)
    # settimeout - интервал, через котороый сервер будет проверять, хочет ли кто к нему подключиться
    serv_sock.settimeout(timeout)
    return serv_sock


def main():
    """Здесь запускается сервер"""

    listen_address, listen_port = arg_parser()

    SERVER_LOGGER.info(
        f'Будет запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет и слушаем порт
    try:
        serv_sock = launch(listen_address, listen_port, TIMEOUT, MAX_CONNECTIONS)
    except Exception:
        SERVER_LOGGER.critical('Не удалось запустить сервер')
        sys.exit(1)
    SERVER_LOGGER.debug(f'Запущен сервер {serv_sock.getsockname()}')

    # Cписок клиентов
    clients = []
    # Очередь сообщений
    messages = []

    # Основной цикл: подключаем клиентов, принимаем сообщения, отправляем сообщения
    while True:
        # Если за время TIMEOUT к серверу никто не подключится, то прерывание OSError
        try:
            client, client_address = serv_sock.accept()
        except OSError:
            pass
        else:
            # Если кто-то подключился, то добавляем его в список clients
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        reading_clients = []
        writing_clients = []
        error_list = []

        # Проверяем наличие ждущих клиентов
        try:
            if clients:
                writing_clients, reading_clients, error_list = \
                    select.select(clients, clients, [], 0)
        except OSError:
            pass

        # Если есть клиенты, готовые отправить сообщения, то принимаем эти
        # сообщения и обрабатываем их.
        # Если сообщение информационное, то оно добавляется в список messages
        if writing_clients:
            for client in writing_clients:
                try:
                    message = get_message(client)
                    SERVER_LOGGER.info(f'Получено сообщение {message}')
                    process_client_message(message, messages, client)
                except NonDictInputError as input_error:
                    SERVER_LOGGER.error(f'{input_error}')
                    clients.remove(client)
                    SERVER_LOGGER.info(f'Клиент {client.getpeername()} отключен от сервера')
                except IncorrectDataRecivedError as data_error:
                    SERVER_LOGGER.error(f'{data_error}')
                    clients.remove(client)
                    SERVER_LOGGER.info(f'Клиент {client.getpeername()} отключен от сервера')
                except json.JSONDecodeError:
                    SERVER_LOGGER.critical(f'Не удалось декодировать сообщение клиента {client}')
                    clients.remove(client)
                    SERVER_LOGGER.info(f'Клиент {client.getpeername()} отключен от сервера')
                except Exception as excep:
                    SERVER_LOGGER.critical(f"Exception class:{excep.__class__}; "
                                           f"exception message: {excep}")
                    clients.remove(client)

        # Если в очереди есть сообщения и есть клиенты, готовые принять сообщения,
        # то оправляем ждущим клиентым каждое сообщение с удалением его из очереди
        if messages and reading_clients:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for client in reading_clients:
                try:
                    send_message(message, client)
                except Exception:
                    SERVER_LOGGER.info(f'Клиент {client.getpeername()} отключился от сервера')
                    clients.remove(client)


if __name__ == '__main__':
    main()
