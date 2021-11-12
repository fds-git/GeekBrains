'''Программа сервера времени'''

from socket import socket, AF_INET, SOCK_STREAM
import time

SERV_SOCK = socket(AF_INET, SOCK_STREAM)
SERV_SOCK.bind(('', 8888))
SERV_SOCK.listen(5)

try:
    while True:
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()
        DATA = CLIENT_SOCK.recv(4096)
        #print(f'Получен запрос на установку соединения от клиента с адресом и портом: {ADDR}')
        print(f'Сообщение {DATA.decode("utf-8")} было отправлено клиентом: {ADDR}')
        MSG = 'Привет, клиент'
        #TIMESTR = time.ctime(time.time()) + "\n"
        #CLIENT_SOCK.send(TIMESTR.encode('utf-8'))
        CLIENT_SOCK.send(MSG.encode('utf-8'))
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()
