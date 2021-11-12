"""
Синхронизация процессов через неименованные каналы Pipe
"""

import time
import multiprocessing


def consumer(pipe):
    """Потребитель - получает элементы из канала"""
    output_p, input_p = pipe
    # Закрыть конец канала, доступный для записи
    input_p.close()
    while True:
        try:
            item = output_p.recv()
        except EOFError:
            break
        # Обработать элемент
        print('извлекаю')
        # Замените эту инструкцию фактической обработкой
        print(item)
        time.sleep(2)
    # Завершение
    print("Потребитель завершил работу")


def producer(sequence_obj, input_pipe):
    """
    Создает элементы и помещает их в канал. Переменная sequence представляет
    итерируемый объект с элементами, которые требуется обработать.
    :param sequence:
    :param input_p:
    :return:
    """
    for item in sequence_obj:
        print('отправляю')
        # Послать элемент в канал
        input_pipe.send(item)
        time.sleep(2)


if __name__ == '__main__':
    # output_p, input_p - кортеж (концы канала)
    OUTPUT_P, INPUT_P = multiprocessing.Pipe()
    # Запустить процесс-потребитель
    CONS_P = multiprocessing.Process(target=consumer, args=((OUTPUT_P, INPUT_P), ))
    CONS_P.start()

    # Закрыть в поставщике конец канала, доступный для чтения
    OUTPUT_P.close()

    # Отправить элементы
    SEQUENCE = [1, 2, 3, 4]
    producer(SEQUENCE, INPUT_P)

    # Сообщить об окончании, закрыв конец канала, доступный для записи
    INPUT_P.close()

    # Дождаться, пока завершится процесс-потребитель
    CONS_P.join()
