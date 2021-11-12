"""Unit-тесты клиента"""

import unittest
from common.constants import RESPONSE, ERROR, USER, ACCOUNT_NAME, \
    TIME, ACTION, PRESENCE, STATUS, ONLINE
from client import make_presence, process_ans


class TestClient(unittest.TestCase):
    '''Класс для тестирования функций файла client.py'''

    def test_make_presense(self):
        """Тест сообщения клиента при подключении к серверу"""
        message = make_presence()
        message[TIME] = 5.2
        self.assertEqual(message, {ACTION: PRESENCE, TIME: 5.2, USER: {ACCOUNT_NAME: 'Guest', STATUS: ONLINE}})

    def test_process_ans_200(self):
        """Тест process_ans при привильном формировании сообщения от сервера и коде 200"""
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_process_ans_400(self):
        """Тест process_ans при привильном формировании сообщения от сервера и коде 400"""
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """Тест process_ans при непривильном формировании сообщения от сервера (нет RESPONSE)"""
        self.assertRaises(ValueError, process_ans, {ERROR: 'WORD'})


if __name__ == '__main__':
    unittest.main()
