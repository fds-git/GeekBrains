'''Программа клиента времени'''

from socket import socket, AF_INET, SOCK_STREAM

CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCK.connect(('localhost', 8888))
MSG = 'Привет, сервер'
CLIENT_SOCK.send(MSG.encode('utf-8'))
DATA = CLIENT_SOCK.recv(4096)
#TIME_BYTES = CLIENT_SOCK.recv(1024)
#print(f"Текущее время: {TIME_BYTES.decode('utf-8')}")
print(f"Сообщение от сервера: {DATA.decode('utf-8')} длиной {len(DATA)} байт")
CLIENT_SOCK.close()

