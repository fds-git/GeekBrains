"""
Программа клиента, бесконечно запрашивающего текущее время
"""

from socket import socket, AF_INET, SOCK_STREAM

SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.connect(('localhost', 8888))

while True:
    TIME_BYTES = SOCK.recv(1024)
    print(f"Текущее время: {TIME_BYTES.decode('utf-8')}")

SOCK.close()
