import urllib.request
import urllib.parse
from typing import Optional

from tg_token import TG_TOKEN
import json
from telegram import Message, get_name
from check_functions import is_correct_whois, has_whois_in_text


def get_hello_text(chat_id: int, group_name: str, name: str) -> str:
    try:
        file_hello = open('templates/hello_text_%s.html' % chat_id, 'r', encoding='UTF-8')
    except:     # TODO продумать обработку разного типа исключений и настроить логирование ошибок
        file_hello = open('templates/hello_text.html', 'r', encoding='UTF-8')
    text = file_hello.read().format(group_name=group_name, name=name)
    file_hello.close()
    return text


def encode_params(**kwargs) -> str:
    params = {}
    for key in kwargs:
        if kwargs[key] is not None:
            params[key] = kwargs[key]
        else:
            continue
    return urllib.parse.urlencode(params)


def send_message(chat_id: int, text: str, message_id: Optional[int] = None):
    bot_url = f"https://api.telegram.org/bot{TG_TOKEN}"
    message_params_encoded = encode_params(chat_id=chat_id, text=text, reply_to_message_id=message_id,
                                           parse_mode='HTML')
    send_url = f"{bot_url}/sendMessage?{message_params_encoded}"
    try:
        urllib.request.urlopen(send_url, timeout=1)
        return f'Success'
    except:     # TODO продумать обработку разного типа исключений и настроить логирование ошибок
        return f'Fail'


def say_hello(message: Message) -> dict:
    result = {}
    for member in message.new_chat_members:
        name = get_name(member)
        text = get_hello_text(message.chat_id, message.group_name, name)
        result[name] = send_message(message.chat_id, text, message.id)
    return result


def send_answer(message: Message):
    if has_whois_in_text(message.text):
        if is_correct_whois(message.text):
            text = "Спасибо, что представились"
        else:
            text = "Вы представились не по правилам, пожалуйста, перепишите свое представление по шаблону: #whois " \
                   "Гаррус 16-10 "
        return send_message(message.chat_id, text, message.id)
    else:
        return None


def lambda_handler(event: dict, context):
    result = {}
    message = Message(event['body-json']['message'])
    if message.new_chat_members:
        result['say_hello'] = say_hello(message)
    elif message.text:
        result['send_answer'] = send_answer(message)
    print(event, result)
    return {
        'statusCode': 200,
        'body': json.dumps('Ok')
    }
