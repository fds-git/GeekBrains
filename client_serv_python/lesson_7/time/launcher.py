"""
Служебный скрипт запуска/останова нескольких клиентских приложений
"""

from subprocess import Popen, CREATE_NEW_CONSOLE


P_LIST = []
server = Popen('python time_server_select.py', creationflags=CREATE_NEW_CONSOLE)
while True:
    USER = input("Запустить 10 клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")

    if USER == 'q':
        server.kill()
        for p in P_LIST:
            p.kill()
        P_LIST.clear()
        break

    elif USER == 's':
        for _ in range(10):

            P_LIST.append(Popen('python time_client_random.py', creationflags=CREATE_NEW_CONSOLE))

        print(' Запущено 10 клиентов')
    elif USER == 'x':
        for p in P_LIST:
            p.kill()
        P_LIST.clear()

