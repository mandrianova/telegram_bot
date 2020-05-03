# Welcome bot
greetings when adding new users to the group. It's all!

Runs on Python 3.8 as a lambda function on AWS.

## For running you need:
1. Create a bot through BotFather, get a token. Set / setprivacy - disable.
2. Create a file tg_token.py and set the variable TG_TOKEN = "token" in it, assigning it the received token. Put the file next to the rest of the scripts.
3. Create an AWS account, get a lambda function using Python 3.8 from scratch. Upload the zip archive with the code there
4. Create an API on AWS and assign it to our lambda function.
5. Select a template for API requests for proper json processing.
6. Configure setWebhook - push: as new messages arrive, the Telegram server sends them to your bot using the AWS API.
7. Add the bot to the group. Add a html-file to the templates folder by analogy with hello_text.html with the name hello_text_ {chat_id} .html, where chat_id is the group id (negative number).

## Unresolved Nuances:
1. For some reason, lambda itself formats the event (from json it is converted to dict, for example, 'false' is automatically replaced by 'False'). 
It is convenient, but it is not clear why this happens and what to expect from it.
2. This installation tutorial is very poor. If it is in demand, I can paint more.
3. The strangest thing is that the maximum number of welcome messages at a time is 3. 
After 3 requests, it fails with a timeout, while with 1 request, the execution speed is 123ms. 
Eliminated the problem with the logic of the formation of messages. 
If you just knock on the finished url, the same problem is still the same.

## About the code itself
- Not perfect, but simple.
- Sending messages can be modified to other scenarios.
- The Message class can be extended to other available fields in the API.
- The get_name function allows you to get a link to a user and call him.
- The hello_text.html template has placeholders {name} - username and {group_name} - chat name. If the chat is private, it will not have {group_name}. Two templates with group id are added as an example.
- The welcome text is processed through the get_hello_text function.


# Приветственный бот
Прост как 3 рубля, никаких дополнительных библиотек не требуется.
Отправляет приветствие при добавлении новых пользователей в группу. Все)

Работает на Python 3.8 как функция [lambda на AWS](https://aws.amazon.com/ru/lambda/).

## Для успешного запуска нужно:
1. Создать бота через BotFather, получить токен. Установить настройку /setprivacy - disable
2. Создать файл tg_token.py и завести в нем переменную TG_TOKEN = "token", назначив ей полученный токен.
Положить файл рядом с остальными скриптами.
3. Завести аккаунт на AWS, завести lambda функцию с использованием Python 3.8 с нуля. Залить туда **zip**-архив с кодом
4. Завести API на AWS и назначить его для нашей lambda-функции.
5. Выбрать template для запросов в API для корректной обработки json.
6. Настроить setWebhook - push: по мере поступления новых сообщений сервер Telegram отправляет их вашему боту на API от AWS.
7. Добавить бота в группу. Добавить в папку templates html-файл по аналогии с hello_text.html с названием hello_text_{chat_id}.html, где chat_id - id группы (отрицательное число).


## Нерешенные нюансы:
1. Почему-то lambda сама форматирует event (из json он преобразуется в dict, значение false, например, автоматически заменяется на False).
Удобно, но непонятно почему так происходит и что от этого ждать.
2. Очень скудный туториал по установке. Если будет востребован, могу расписать подробнее.
3. Самое странное, максимальное количество приветственных сообщений за раз - 3 штуки. После 3 запросов падает с таймаутом, при этом при 1 запросе скорость выполнения 123ms. Исключила проблему с логикой работы формирования сообщений.
Если просто стучать по готовым url, все равно та же проблема.


## Про сам код
- Не идеален, но прост.
- Отправку сообщений можно доработать на другие сценарии.
- Класс **Message** можно развить на остальные доступные поля в API.
- Функция **get_name** позволяет получить ссылку на пользователя и позвать его.
- В шаблоне **hello_text.html** есть плейсхолдеры **{name}** - имя пользователя и **{group_name}** - имя чата. Если чат приватный, у него не будет {group_name}. Два шаблона с id группы добавлены для примера.
- Текст приветствия обрабатывается через функцию **get_hello_text**.

## Дополнительные функции

### Выдача информации из каталога по запросу
С 03.05.2020 добавлена дополнительная функция для местного чатика - получение информации о местных магазинах.
Каталог в репозитории не представлен, но это csv файл с разделителем ";", формат полей:
"name;address;link;phone;info;category".

Работает на русском, позволяет по названию магазина получить его адрес, ссылку, телефон и дополнительную информацию.

Ключевые слова, на которые откликается бот указаны в [check_functions.has_request_to_bot]('/blob/master/check_functions.py')


