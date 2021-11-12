"""
Синхронизация потоков при помощи семафоров
"""

import time
import random
import threading

# Необязательный параметр при создании семафора - внутренний счётчик.
# По умолчанию равен 1.
SEMAPHORE = threading.Semaphore(0)


def consumer():
    """Потребитель"""
    print("Потребитель ждёт...")
    # Захватить семафор
    # уменьшить зн-е счетчика на 1
    # как бы уснуть - уйти в ожидание
    SEMAPHORE.acquire()
    print(f"Потребитель: получено значение {ITEM}")


def producer():
    """Поставщик"""
    global ITEM
    time.sleep(5)
    # Создать случайное значение
    ITEM = random.randint(0, 1000)
    print(f"Поставщик: создано значение {ITEM}")
    
    # Освободить семафор (при этом внутренний счетчик увеличивается на 1)
    # Когда счётчик семафора становится больше нуля, то ожидающий поток просыпается
    # увеличть зн-е счетчика на 1
    SEMAPHORE.release()


if __name__ == '__main__':
    for _ in range(5):
        THR_1 = threading.Thread(target=producer)
        THR_2 = threading.Thread(target=consumer)
        THR_1.start()
        THR_2.start()
        THR_1.join()
        THR_2.join()
    print("Завершено")
