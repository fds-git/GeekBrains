"""Задание 2
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт,
автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена
(price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра."""
import json

DATA_1 = {
    'item': 'Принтер',
    'quantity': 7,
    'price': 7800,
    'buyer': 'Иванов А.А.',
    'date': '23.05.2019'
}

DATA_2 = {
    'item': 'Сканнер',
    'quantity': 10,
    'price': 13000,
    'buyer': 'Петров В.А.',
    'date': '17.02.2019'
}

DATA_3 = {
    'item': 'Компьютер',
    'quantity': 10,
    'price': 200000,
    'buyer': 'Сидоров А.В.',
    'date': '27.08.2019'
}


def write_order_to_json(data_dict):
    """Функция считывает данные из файла, переводит их в словарь,
    добавляет новые данные в словарь и записывает обратно"""
    with open('orders1.json') as f_n:
        obj = json.load(f_n)
        obj['orders'].append(data_dict)
    with open('orders1.json', 'w') as f_n:
        # ensure_ascii=False чтобы русские буквы воспринял
        json.dump(obj, f_n, sort_keys=True, indent=4, ensure_ascii=False)


write_order_to_json(DATA_2)
