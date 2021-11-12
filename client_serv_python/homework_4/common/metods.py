'''Описаны функции, которые используются на клиенте и сервере'''

import json
from common.constants import ENCODING, MAX_LENGTH


def send_message(message, socket_dst):
    '''Функция отправки сообщения. Получает словарь,
    переводит в строку, затем переводит в байты (кодировка UTF-8)
    и отправляет'''
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    socket_dst.send(encoded_message)


def get_message(socket_src):
    '''Функция принятия сообщения. Принимает байты, переводит в строку
    (кодировка UTF-8), затем переводит в словарь и возвращает результат'''
    encoded_response = socket_src.recv(MAX_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def validate_ip(ip_addr):
    '''Функция проверяет является ли выражение возможным IP адресом'''
    ip_addr = ip_addr.split('.')
    if len(ip_addr) != 4:
        return False
    for addr_part in ip_addr:
        if not addr_part.isdigit():
            return False
        addr_part = int(addr_part)
        if addr_part < 0 or addr_part > 255:
            return False
    return True


def get_pos_ind(array):
    '''Возвращает список с индексами полодительных чисел массива array'''
    result = []
    for i in range(len(array)):
        if array[i] > 0:
            result.append(i)
    return result
