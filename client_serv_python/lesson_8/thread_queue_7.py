"""
Обмен данными при помощи очередей
"""

from threading import Thread
from queue import Queue    


class WorkerThread(Thread):
    """Поток с очередью"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_queue = Queue()

    def send(self, item):
        """Положить объект в очередь"""
        self.input_queue.put(item)

    def close(self):
        """Закрыть очередь"""
        self.input_queue.put(None)
        self.input_queue.join()

    def run(self):
        while True:
            item = self.input_queue.get()
            if item is None:
                break
            # Обработать элемент
            # (замените инструкцию print какими-нибудь полезными операциями)
            print(item)
            self.input_queue.task_done()
        # Конец. Сообщить, что сигнальная метка была принята, и выйти
        self.input_queue.task_done()
        return


# Пример использования
WT_OBJ = WorkerThread()
WT_OBJ.start()
# Отправить элемент на обработку (с помощью очереди)
WT_OBJ.send("hello")
WT_OBJ.send("world")
WT_OBJ.close()
