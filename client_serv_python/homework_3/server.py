'''Серверная часть'''
import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
from common.metods import send_message, get_message, validate_ip
from common.constants import RESPONDEFAULT_IP_ADDRESSSE, ERROR, DEFAULT_LISTEN_PORT, \
    MAX_CONNECTIONS, ACTION, TIME, PRESENCE, USER, ACCOUNT_NAME, RESPONSE


def process_client_message(message):
    '''Функция принимает сообщение (словарь) от клиента,
    проверяет правильность сообщения и возвращает словарь-результат'''
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }


def launch(listen_address, listen_port):
    '''Функция запуска сервера'''
    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.bind((listen_address, listen_port))
    serv_sock.listen(MAX_CONNECTIONS)
    return serv_sock


def main():
    '''Обработка параметров, введенных с консоли'''
    # Определяем, кокой порт будем слушать
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_LISTEN_PORT
            print(f'Сервер будет прослушивать порт по умолчанию {DEFAULT_LISTEN_PORT}')
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'Диапазон возможных портов от 1024 до 65535.')
        sys.exit(1)

    # Определяем какой адрес будем слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            if not validate_ip(listen_address):
                print('Неправильный IP-адресс')
                sys.exit(1)
            else:
                print(f'Сервер примет соединение с клиентом с адресом {listen_address}')
        else:
            listen_address = ''
            print('Сервер примет соединение с любым клиентом')

    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет и слушаем порт

    serv_sock = launch(listen_address, listen_port)

    while True:
        client_sock, client_address = serv_sock.accept()
        print(f'К серверу подключен клиент с адресом {client_address}')
        try:
            message = get_message(client_sock)
            print(message)
            response = process_client_message(message)
            send_message(response, client_sock)
            client_sock.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client_sock.close()


if __name__ == '__main__':
    main()
