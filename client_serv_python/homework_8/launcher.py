"""Лаунчер"""

import subprocess

PROCESSES = []

while True:
    COMMAND = input('Возможные команды:\n'
                    's - запустить сервер и клиенты;\n'
                    'k - отключить сервер и клиенты;\n'
                    'e - отключить сервер и клиенты и выйти.\n'
                    '>>> ')

    if COMMAND == 's':
        PROCESSES.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))

        PROCESSES.append(subprocess.Popen('python client.py -n u1',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESSES.append(subprocess.Popen('python client.py -n u2',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESSES.append(subprocess.Popen('python client.py -n u3',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif COMMAND == 'e':
        while PROCESSES:
            PROCESSES.pop().kill()
        break

    elif COMMAND == 'k':
        while PROCESSES:
            PROCESSES.pop().kill()
