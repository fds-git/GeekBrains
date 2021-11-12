"""
TCP-сервер, обрабатывающий каждого клиента в отдельном потоке
"""


import socket
import threading
import socketserver


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """Создаем класс-обработчик сообщений пользователя"""

    def handle(self):
        data = str(self.request.recv(1024), 'utf-8')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'utf-8')
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    Потоковый сервер. Достаточно создать класс без "внутренностей"
    Обратите внимание на использование класса-примеси ThreadingMixIn
    """
    pass


def client(ip_addr, port, message):
    """Создадим простого 'клиента'"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip_addr, port))
        sock.sendall(bytes(message, 'utf-8'))
        response = str(sock.recv(1024), 'utf-8')
        print(f"Сервер ответил: {response}")


if __name__ == "__main__":
    # Порт 0 позволяет выбрать незанятый порт автоматически
    HOST, PORT = "localhost", 0

    SERVER = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with SERVER:
        IP_ADDR, PORT = SERVER.server_address

        # Запускаем поток для цикла сервера.
        # Этот поток будет создавать поток для каждого клиента
        SERVER_THREAD = threading.Thread(target=SERVER.serve_forever,
                                         name='thread.server')

        # Ставим флаг daemon, чтобы сервер завершился, когда завершится основная программа
        SERVER_THREAD.daemon = True
        SERVER_THREAD.start()
        print(f"Сервер запущен в потоке: {SERVER_THREAD.name} по адресу {IP_ADDR}:{PORT}")

        client(IP_ADDR, PORT, "Терминал-1 приветствует Вас!")
        client(IP_ADDR, PORT, "Привет от терминала-2!")
        client(IP_ADDR, PORT, "А третий терминал не будет здороваться...")

        SERVER.shutdown()
