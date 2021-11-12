"""Простой поток"""

import time
from threading import Thread


def clock(interval):
    """Функция, которая может быть запущена в потоке"""

    while True:
        print(interval)
        print(f"Текущее время: {time.ctime()}")
        time.sleep(interval)


THR = Thread(target=clock, args=(3, ))

"""
Обычно Python-приложение не завершается, пока работает хоть один его поток. 
Но есть особые потоки, которые не мешают закрытию программы и останавливается вместе с ней. 
Их называют демонами (daemons). Проверить, является ли поток демоном, можно методом isDaemon(). 
Если является, метод вернёт истину.
"""

THR.daemon = True
THR.start()
THR.join()
