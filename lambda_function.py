import os
import urllib.request
import urllib.parse
from typing import Optional

from tg_token import TG_TOKEN
import json
from telegram import Message, get_name


def get_hello_text(chat_id: int, group_name: str, name: str) -> str:
    if os.path.exists('templates/hello_text_%s.html' % chat_id):
        file_hello = open('templates/hello_text_%s.html' % chat_id, 'r', encoding='UTF-8')
    else:
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
    except:
        return f'Fail'


def say_hello(message: Message) -> dict:
    result = {}
    for member in message.new_chat_members:
        name = get_name(member)
        text = get_hello_text(message.chat_id, message.group_name, name)
        result[name] = send_message(message.chat_id, text, message.id)
    return result


def lambda_handler(event: dict, context):
    result = {}
    message = Message(event['body-json']['message'])
    if message.new_chat_members:
        result['say_hello'] = say_hello(message)
    print(event, result)
    return {
        'statusCode': 200,
        'body': json.dumps('Ok')
    }
