"""
Эхо-сервер, обрабатывающий "одновременно" несколько клиентов
Обработка клиентов осуществляется функцией select
"""

import select
from socket import socket, AF_INET, SOCK_STREAM


def read_requests(read_clients, all_clients):
    """Чтение запросов из списка клиентов"""

    responses = {}

    for sock in read_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except Exception:
            print(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
            all_clients.remove(sock)

    return responses


def write_responses(requests, clients_write, all_clients):
    """Эхо-ответ сервера клиентам, от которых были запросы"""

    for sock in clients_write:
        if sock in requests:
            try:
                resp = requests[sock].upper()
                #print(resp)
                sock.send(resp.encode('utf-8'))
            except Exception:
                # sock.fileno() - вернуть дескриптор файла сокетов (небольшое целое число)
                # sock.getpeername() - получить IP-адрес и номер порта клиента
                print(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
                sock.close()
                all_clients.remove(sock)


def mainloop():
    """Основной цикл обработки запросов клиентов"""

    address = ('', 10000)
    all_clients = []

    with socket(AF_INET, SOCK_STREAM) as sock:
        # sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(address)
        sock.listen(5)
        sock.settimeout(0.2)
        while True:
            try:
                conn, addr = sock.accept()
            except OSError as err:
                pass
            else:
                print(f"Получен запрос на соединение от {str(addr)}")
                all_clients.append(conn)
            finally:
                wait = 0
                clients_read = []
                clients_write = []
                try:
                    clients_read, clients_write, errors = \
                        select.select(all_clients, all_clients, [], wait)
                    #print(clients_read)
                #   print(clients_write)
                except Exception:
                    pass

                requests = read_requests(clients_read, all_clients)
                print(requests)
                if requests:
                    #print(requests)
                    write_responses(requests, clients_write, all_clients)


print('Эхо-сервер запущен!')
mainloop()
