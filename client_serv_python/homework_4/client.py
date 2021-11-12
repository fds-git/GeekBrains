'''Клиентская часть'''
import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import time
from common.metods import send_message, get_message, validate_ip
from common.constants import RESPONSE, ERROR, DEFAULT_LISTEN_ADDR, DEFAULT_LISTEN_PORT, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, STATUS, ONLINE


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
    return message


def process_ans(message):
    '''Функция обработки ответа от сервера'''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def connect(host, port):
    '''Функция подключения клиента к серверу с параметрами (host, port)'''
    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect((host, port))
    return client_sock


def disconnect(client_sock):
    '''Функция отключения клиента от сервера'''
    client_sock.close()


def main():
    '''Обрабатываем параметры, введенные в консоли'''
    try:
        server_address = sys.argv[1]
        if not validate_ip(server_address):
            print('Неправильный IP-адресс')
            sys.exit(1)
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            print('Порт - число в диапазоне от 1024 до 65535.')
            sys.exit(1)
        print(f'Будет произведено подключение к {server_address}: {server_port}')
    except IndexError:
        print('Неправильные параметры, будет произведено '
              f'подключение к {DEFAULT_LISTEN_ADDR}: {DEFAULT_LISTEN_PORT}')
        server_address = DEFAULT_LISTEN_ADDR
        server_port = DEFAULT_LISTEN_PORT

    # Инициализация сокета и обмен
    try:
        client_sock = connect(server_address, server_port)
    except ConnectionRefusedError:
        # Если сервер ждет соединения от клиента с другим ip адресом (-p 'адрес'), то ошибка
        print('Подключение не установлено, т.к. конечный компьютер отверг запрос на подключение')
        sys.exit(1)
    # Отправка сообщения серверу о подключении
    send_message(make_presence(), client_sock)

    try:
        print(process_ans(get_message(client_sock)))
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
