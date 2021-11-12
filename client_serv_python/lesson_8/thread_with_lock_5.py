"""Потоки с блокировками и без"""

import threading

SHARED_RESOURCE_WITH_LOCK = 0
SHARED_RESOURCE_WITH_NO_LOCK = 0
COUNT = 5
SHARED_RESOURCE_LOCK = threading.Lock()


def increment_with_lock():
    """Инкремент с блокировками"""
    global SHARED_RESOURCE_WITH_LOCK
    for _ in range(COUNT):
        SHARED_RESOURCE_LOCK.acquire()
        SHARED_RESOURCE_WITH_LOCK += 1
        #print(shared_resource_with_lock)
        SHARED_RESOURCE_LOCK.release()


def decrement_with_lock():
    """Декремент с блокировками"""
    global SHARED_RESOURCE_WITH_LOCK
    for _ in range(COUNT):
        SHARED_RESOURCE_LOCK.acquire()
        SHARED_RESOURCE_WITH_LOCK -= 1
        #print(shared_resource_with_lock)
        SHARED_RESOURCE_LOCK.release()


def increment_without_lock():
    """Инкремент без блокировок"""
    global SHARED_RESOURCE_WITH_NO_LOCK
    for _ in range(COUNT):
        SHARED_RESOURCE_WITH_NO_LOCK += 1
        print(SHARED_RESOURCE_WITH_NO_LOCK)


def decrement_without_lock():
    """Декремент без блокировок"""
    global SHARED_RESOURCE_WITH_NO_LOCK
    for _ in range(COUNT):
        SHARED_RESOURCE_WITH_NO_LOCK -= 1
        print(SHARED_RESOURCE_WITH_NO_LOCK)


if __name__ == "__main__":
    #THR_1 = threading.Thread(target=increment_with_lock)
    #THR_2 = threading.Thread(target=decrement_with_lock)
    THR_3 = threading.Thread(target=increment_without_lock)
    THR_4 = threading.Thread(target=decrement_without_lock)
    #THR_1.start()
    #THR_2.start()
    THR_3.start()
    THR_4.start()
    #THR_1.join()
    #THR_2.join()
    THR_3.join()
    THR_4.join()
