import csv


def load_catalog():
    full_catalog = {}
    category_list = {}
    with open('mvl.csv', 'r', encoding='utf-8-sig') as csv_file:
        catalog = csv.DictReader(csv_file, dialect='excel', delimiter=';')
        for row in catalog:
            key = row.pop('name')
            category = row.pop('category')
            if category_list.get(category):
                tmp_list = category_list.get(category)
            else:
                tmp_list = []
            tmp_list.append(key)
            category_list[category] = tmp_list
            full_catalog[key] = dict(row)
    return full_catalog, category_list


class Catalog:
    key_words = {'телефон': 'phone', 'адрес': 'address', 'ссылк': 'link', 'где': 'address', 'номер': 'phone'}

    def __init__(self, text):
        self.text = text
        self.full_catalog, self.category_list = load_catalog()

    @property
    def name(self):
        text = self.text.lower()
        for name in self.full_catalog:
            check_name = name.lower()
            if check_name[0:-1] in text:
                return name
        return None

    @property
    def category(self):
        text = self.text.lower()
        for category in self.category_list:
            check_category = f" {category.lower()}"
            if len(check_category) > 2:
                check_category = check_category[0:-1]
            if check_category in text:
                return category
        return None

    @property
    def key(self):
        for key in self.key_words:
            if key in self.text.lower():
                return self.key_words[key]
        return 'info'

    def get_help(self):
        if self.name:
            return self.full_catalog[self.name][self.key]
        elif self.category:
            return "\n".join(sorted(self.category_list[self.category]))
        list_names = ', '.join(sorted(self.full_catalog.keys()))
        return f'Люди, помогите! \nЯ знаю только про: {list_names}. \n<b>Можете добавлять данные ' \
               f'<a href="https://docs.google.com/spreadsheets/d/1o9SfeTEHcML2oAhA93hQAu3YhBZc9n8O_c_VpJJtc9c/edit#gid' \
               f'=1906406446">в эту таблицу</a> и помечать новое зеленым цветом.</b>'
