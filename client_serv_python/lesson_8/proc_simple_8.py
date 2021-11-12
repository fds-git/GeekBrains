"""Мультипроцессинг с функцией"""

import time
import multiprocessing


def clock(interval):
    """Простая функция"""
    while True:
        print(f"The time is {time.ctime()}")
        time.sleep(interval)


if __name__ == "__main__":
    PROC = multiprocessing.Process(target=clock, args=(1, ))
    PROC.start()
