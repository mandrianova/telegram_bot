import csv


def get_list_names():
    list_names = []
    with open('mvl.csv', 'r', encoding='utf-8-sig') as csv_file:
        catalog = csv.DictReader(csv_file, dialect='excel', delimiter=';')
        for row in catalog:
            list_names.append(row["name"])
    return list_names


class Catalog:
    key_words = {'телефон': 'phone', 'адрес': 'address', 'ссылк': 'link', 'где': 'address', 'номер': 'phone'}

    def __init__(self, text):
        self.text = text

    @property
    def name(self):
        text = self.text.lower()
        for name in get_list_names():
            check_name = name.lower()
            if check_name in text:
                return name
        return None

    @property
    def key(self):
        for key in self.key_words:
            if key in self.text.lower():
                return self.key_words[key]
        return 'info'

    def get_help(self):
        if self.name:
            with open('mvl.csv', 'r', encoding='utf-8-sig') as csv_file:
                catalog = csv.DictReader(csv_file, dialect='excel', delimiter=';')
                for row in catalog:
                    if row['name'] == self.name:
                        return row[self.key]
        list_names = ', '.join(get_list_names())
        return f'Люди, помогите! Я знаю только про: {list_names}'
