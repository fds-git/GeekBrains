"""Unit-тесты утилит"""

import sys
import os
import unittest
import json
from common.constants import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
from common.metods import get_message, send_message, validate_ip
sys.path.append(os.path.join(os.getcwd(), '..'))


class TestSocket:
    '''Класс для имитации отправки сообщений черех сокет'''
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        """Отправить данные в сокет"""
        json_test_message = json.dumps(self.test_dict)
        # кодирует сообщение
        self.encoded_message = json_test_message.encode(ENCODING)
        # сохраняем что должно было отправлено в сокет
        self.receved_message = message_to_send

    def recv(self, max_len):
        """Получить данные из сокета"""
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestsMetods(unittest.TestCase):
    '''Класс для тестирования функций из metods.py'''
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 5.2,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_message(self):
        """
        Тестируем корректность работы фукции отправки,
        создадим тестовый сокет и проверим корректность отправки словаря
        :return:
        """
        # экземпляр тестового словаря, хранит собственно тестовый словарь
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        send_message(self.test_dict_send, test_socket)
        # проверка корретности кодирования словаря.
        # сравниваем результат довренного кодирования и результат от тестируемой функции
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)
        # дополнительно, проверим генерацию исключения, при не словаре на входе.
        self.assertRaises(TypeError, send_message, test_socket, 1111)

    def test_get_message(self):
        """
        Тест функции приёма сообщения
        :return:
        """
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # тест корректной расшифровки корректного словаря
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)

    def test_validate_ip_1(self):
        """Тест validate_ip c параметром 192.168.2.1"""
        self.assertEqual(validate_ip('192.168.2.1'), True)

    def test_validate_ip_2(self):
        """Тест validate_ip c параметром 292.168.2.1"""
        self.assertEqual(validate_ip('292.168.2.1'), False)

    def test_validate_ip_3(self):
        """Тест validate_ip c параметром 168.2.1"""
        self.assertEqual(validate_ip('168.2.1'), False)

    def test_validate_ip_4(self):
        """Тест validate_ip c параметром 192.168.2,1"""
        self.assertEqual(validate_ip('192.168.2,1'), False)


if __name__ == '__main__':
    unittest.main()
