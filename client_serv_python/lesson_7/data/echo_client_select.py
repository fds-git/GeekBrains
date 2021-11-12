"""Программа клиента, отправляющего/читающего простые текстовые сообщения на сервер"""

from socket import socket, AF_INET, SOCK_STREAM

ADDRESS = ('localhost', 10000)


def echo_client():
    """Общение с сервером"""
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(ADDRESS)
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            sock.send(msg.encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            print(f"Ответ: {data}")


if __name__ == '__main__':
    echo_client()
