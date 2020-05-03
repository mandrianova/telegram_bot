import unittest
from lambda_function import get_hello_text, send_message, encode_params, say_hello
from telegram import Message, get_name
import urllib.request
import os
from check_functions import has_whois_in_text, is_correct_whois


event = {'body-json':
             {'update_id': 243589604,
              'message':
                  {'message_id': 405,
                   'from': {'id': 1111, 'is_bot': False, 'first_name': 'Ivan', 'last_name': 'Ivanov',
                            'username': 'IvanIvanov', 'language_code': 'ru'},
                   'chat': {'id': -426886186, 'title': 'test_bot', 'type': 'group',
                            'all_members_are_administrators': True},
                   'date': 1587907791,
                   'new_chat_participant': {'id': 1111, 'is_bot': False, 'language_code': 'ru'},
                   'new_chat_member': {'id': 1111, 'is_bot': False, 'language_code': 'ru'},
                   'new_chat_members': [{'id': 1111, 'username': 'AnnaIvanova', 'last_name': 'Ivanova', 'is_bot': False,
                                         'language_code': 'ru'},
                                        {'id': 1112, 'is_bot': False, 'language_code': 'ru'},
                                        {'id': 1113, 'first_name': 'Sasha', 'is_bot': False, 'language_code': 'ru'},
                                        {'id': 1114, 'last_name': 'Sidorov', 'is_bot': False, 'language_code': 'ru'},
                                        {'id': 1115, 'first_name': 'Igor', 'last_name': 'Chi', 'is_bot': False,
                                         'language_code': 'ru'}
                                        ]
                   }
              },
         }
message = Message(event['body-json']['message'])


class TestFunctions(unittest.TestCase):

    def test_encode_params_without_message_id(self):
        self.assertEqual(encode_params(chat_id=-123, text="Мама мыла раму", parse_mode="HTML", message_id=None),
                         "chat_id=-123&text=%D0%9C%D0%B0%D0%BC%D0%B0+%D0%BC%D1%8B%D0%BB%D0%B0+%D1%80%D0%B0%D0%BC%D1%83&parse_mode=HTML")

    def test_encode_params_with_message_id(self):
        self.assertEqual(encode_params(chat_id=-123, text="Мама мыла раму", parse_mode="HTML", message_id=25),
                         "chat_id=-123&text=%D0%9C%D0%B0%D0%BC%D0%B0+%D0%BC%D1%8B%D0%BB%D0%B0+%D1%80%D0%B0%D0%BC%D1%83&parse_mode=HTML&message_id=25")

    def test_get_hello_new_text(self):
        with open('templates/hello_text_-53.html', 'w', encoding='UTF-8') as new_hello:
            new_hello.write('Приветствуем в чате {group_name} нового участника {name}')
        self.assertEqual(get_hello_text(-53, 'check', 'first_name'),
                         "Приветствуем в чате check нового участника first_name")
        os.remove('templates/hello_text_-53.html')
        with open('templates/hello_text_-24.html', 'w', encoding='UTF-8') as new_hello:
            new_hello.write('Приветствуем в чате нового участника')
        self.assertEqual(get_hello_text(-24, 'check', 'first_name'),
                         "Приветствуем в чате нового участника")
        os.remove('templates/hello_text_-24.html')

    def test_get_hello_default_text(self):
        self.assertEqual(get_hello_text(-53, 'check', 'first_name'), "Добро пожаловать в чат check, first_name.")

    def test_send_message(self):
        try:
            urllib.request.urlopen('https://api.telegram.org/', timeout=1)
            self.assertEqual(send_message(142718925, "Тест"),
                             'Success')
        except:
            self.assertEqual(send_message(142718925, "Тест"),
                             'Fail')

    def test_say_hello_many_members(self):

        try:
            urllib.request.urlopen('https://api.telegram.org/', timeout=1)
            self.assertEqual(say_hello(message), {"<a href='tg://user?id=1114'>Sidorov</a>": 'Success',
                                                  "<a href='tg://user?id=1115'>Igor Chi</a>": 'Success',
                                                  "<a href='tg://user?id=1113'>Sasha</a>": 'Success',
                                                  "<a href='tg://user?id=1112'>Неизвестный пользователь</a>": 'Success',
                                                  '@AnnaIvanova, Ivanova': 'Success'})
        except:
            self.assertEqual(say_hello(message), {"<a href='tg://user?id=1114'>Sidorov</a>": 'Fail',
                                                  "<a href='tg://user?id=1115'>Igor Chi</a>": 'Fail',
                                                  "<a href='tg://user?id=1113'>Sasha</a>": 'Fail',
                                                  "<a href='tg://user?id=1112'>Неизвестный пользователь</a>": 'Fail',
                                                  '@AnnaIvanova, Ivanova': 'Fail'})

    def test_get_name(self):
        user_without_username = {'id': 1115, 'first_name': 'Igor', 'last_name': 'Chi', 'is_bot': False,
                                 'language_code': 'ru'}
        self.assertEqual(get_name(user_without_username), "<a href='tg://user?id=1115'>Igor Chi</a>")
        user_without_name = {'id': 1115, 'is_bot': False, 'language_code': 'ru'}
        self.assertEqual(get_name(user_without_name), "<a href='tg://user?id=1115'>Неизвестный пользователь</a>")
        user_full = {'id': 1115, 'username': 'sun', 'first_name': 'Igor', 'last_name': 'Chi', 'is_bot': False,
                     'language_code': 'ru'}
        self.assertEqual(get_name(user_full), "@sun, Igor Chi")

    def test_has_whois_in_text(self):
        self.assertEqual(has_whois_in_text('Привет'), False)
        self.assertEqual(has_whois_in_text('Привет всем! #whois Маша'), True)

    def test_is_correct_whois(self):
        self.assertEqual(is_correct_whois('Привет #whois'), False)
        self.assertEqual(is_correct_whois('Привет всем! #whois Маша'), False)
        self.assertEqual(is_correct_whois('Привет всем! #whois Маша 23465-827346'), True)
        self.assertEqual(is_correct_whois('Привет всем! #whois Маша и дальше я продолжила писать свое письмо'), False)
        self.assertEqual(is_correct_whois('#whois 13-666 магия'), True)
        self.assertEqual(is_correct_whois('#whois чёрная магия'), False)


if __name__ == '__main__':
    unittest.main()
