class Message:
    def __init__(self, message):
        self.message = message

    @property
    def id(self):
        return self.message.get('message_id')

    @property
    def chat_id(self):
        return self.message['chat']['id']

    @property
    def group_name(self):
        if self.message['chat']['type'] != "private":
            return self.message['chat']['title']
        else:
            return False

    @property
    def new_chat_members(self):
        if self.message.get('new_chat_members'):
            return self.message.get('new_chat_members')
        else:
            return False

    @property
    def text(self):
        return self.message.get('text')


def get_name(user: dict) -> str:
    first_name = user.get('first_name')
    last_name = user.get('last_name')
    username = user.get('username')
    user_id = user.get('id')
    if first_name and last_name:
        name = f"{first_name} {last_name}"
    elif first_name:
        name = first_name
    elif last_name:
        name = last_name
    else:
        name = "Неизвестный пользователь"
    if username:
        return f"@{username}, {name}"
    else:
        return "<a href='tg://user?id={}'>{}</a>".format(user_id, name)


