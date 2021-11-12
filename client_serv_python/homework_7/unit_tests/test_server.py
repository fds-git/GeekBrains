"""Unit-тесты сервера"""

import unittest
from common.constants import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import process_client_message


class TestServer(unittest.TestCase):
    '''Класс для тестирования функций файла server.py'''

    error_message = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    valid_message = {RESPONSE: 200}

    def test_good(self):
        """Сообщение клиента сформировано правильно"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 5.2, USER: {ACCOUNT_NAME: 'Guest'}}), self.valid_message)

    def test_no_action(self):
        """В сообщении клиента нет ACTION"""
        self.assertEqual(process_client_message(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.error_message)

    def test_wrong_action(self):
        """В сообщении клиента ACTION != PRESENCE"""
        self.assertEqual(process_client_message(
            {ACTION: 'Word', TIME: 5.2, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_message)

    def test_no_time(self):
        """В сообщении клиента нет TIME"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_message)

    def test_no_user(self):
        """В сообщении клиента нет USER"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 5.2}), self.error_message)

    def test_wrong_user(self):
        """В сообщении клиента ACCOUNT_NAME != Guest"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 5.2, USER: {ACCOUNT_NAME: 'NotGuest'}}), self.error_message)


if __name__ == '__main__':
    unittest.main()
