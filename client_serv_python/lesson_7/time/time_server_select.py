"""
Сервер времени, обрабатывающий "одновременно" несколько клиентов
Обработка клиентов осуществляется функцией select
"""

import time
import select
from socket import socket, AF_INET, SOCK_STREAM


def new_listen_socket(address):
    """Инициируем серверный сокет"""
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(10)
    # проверяем есть ли новые клиенты
    # проверяем есть ли данные
    sock.settimeout(10)
    return sock


def mainloop():
    """Основной цикл обработки запросов клиентов"""
    address = ('', 8888)
    all_clients = []
    sock = new_listen_socket(address)

    while True:
        try:
            # Проверка: кто-либо ожидает подключения к серверу
            conn, addr = sock.accept()
            print(conn)
        # Подключение каждого клиента будет с периодом timeout
        except OSError:
            # Если никто не хочет подключиться, то попадаем сюда
            pass
        else:
            print(f"Получен запрос на соединение с {str(addr)}")
            # вносим в список добавившегося клиента
            all_clients.append(conn)
        finally:

            clients_write = []
            try:
                clients_read, clients_write, errors = select.select([], all_clients, [], 0)

            except Exception:
                pass

            for client in clients_write:
                # определяем время
                time_str = time.ctime(time.time()) + "\n"
                try:
                    # отправляем время клиенту
                    client.send(time_str.encode('utf-8'))

                except Exception:
                    # Если клиент отключился, удаляем его
                    all_clients.remove(client)


print('Эхо-сервер запущен!')
mainloop()
