'''Серверная часть'''
import sys
import json
import socket
from decorators import log
from errors import IncorrectDataRecivedError, NonDictInputError
from socket import socket, AF_INET, SOCK_STREAM
from common.metods import send_message, get_message, validate_ip
from common.constants import RESPONDEFAULT_IP_ADDRESSSE, ERROR, DEFAULT_LISTEN_PORT, \
    MAX_CONNECTIONS, ACTION, TIME, PRESENCE, USER, ACCOUNT_NAME, RESPONSE
from logging import getLogger
import logs.server_log_settings

# Подключаем серверный логгер из server_log_settings
SERVER_LOGGER = getLogger('server')


@log
def process_client_message(message):
    '''Функция принимает сообщение (словарь) от клиента,
    проверяет правильность сообщения и возвращает словарь-результат'''
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


@log
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
            listen_port = sys.argv[sys.argv.index('-p') + 1]
            if not listen_port.isdigit():
                SERVER_LOGGER.critical('Порт должен задаваться числом')
                sys.exit(1)
            listen_port = int(listen_port)
        else:
            listen_port = DEFAULT_LISTEN_PORT
            SERVER_LOGGER.error(f'Номер порта не задан. Сервер будет прослушивать порт по умолчанию {DEFAULT_LISTEN_PORT}')
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical('После параметра -\'p\' необходимо указать номер порта')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical('Диапазон возможных портов от 1024 до 65535')
        sys.exit(1)

    # Определяем какой адрес будем слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            if not validate_ip(listen_address):
                SERVER_LOGGER.critical('IP-адрес сервера задан неверно')
                sys.exit(1)
            else:
                SERVER_LOGGER.debug(f'Сервер примет соединение с клиентом с адресом {listen_address}')
        else:
            listen_address = ''
            SERVER_LOGGER.debug('Сервер примет соединение с любым клиентом')

    except IndexError:
        SERVER_LOGGER.critical('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер')
        sys.exit(1)

    # Готовим сокет и слушаем порт
    try:
        serv_sock = launch(listen_address, listen_port)
    except:
        SERVER_LOGGER.critical('Не удалось запустить сервер')
        sys.exit(1)
    SERVER_LOGGER.debug(f'Запущен сервер {serv_sock.getsockname()}')

    while True:
        client_sock, client_address = serv_sock.accept()
        client_name = client_sock.getpeername()
        server_name = client_sock.getsockname()
        SERVER_LOGGER.debug(f'К серверу подключен клиент {client_name}')
        try:
            message = get_message(client_sock)
            SERVER_LOGGER.debug(f'Получено сообщение от клиента {client_name}:  {message}')
            response = process_client_message(message)
            send_message(response, client_sock)
            SERVER_LOGGER.debug(f'Отправлен ответ клиенту {client_name}: {response}')
        except NonDictInputError as input_error:
            SERVER_LOGGER.error(f'{input_error}')
        except IncorrectDataRecivedError as data_error:
            SERVER_LOGGER.error(f'{data_error}')
        except json.JSONDecodeError:
            SERVER_LOGGER.critical(f'Не удалось декодировать сообщение клиента {client_name}')
        client_sock.close()
        SERVER_LOGGER.debug(f'Клиент {client_name} отключен от сервера {server_name}')


if __name__ == '__main__':
    main()
