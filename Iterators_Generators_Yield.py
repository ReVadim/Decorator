import requests
import json
import hashlib
from datetime import datetime


def simple_logger_decorator(main_func):

    def new_function(*args, **kwargs):
        result = main_func(*args, **kwargs)
        log = f'Вызвана функция "{main_func.__name__}" с аргументами: {args}, {kwargs}.' \
              f'Результат выполнения: {result}.\nВызов функции произведен: {datetime.now()}'
        print(log)
        with open('log_list.txt', 'a', encoding='utf-8') as f:
            f.write(f"{log}\n")

        return result

    return new_function


netology_link = 'https://raw.githubusercontent.com/mledoze/countries/master/countries.json'
wiki_link = 'https://en.wikipedia.org/wiki/'


class Downloader:

    def __init__(self, url):
        self.url = url
        response = requests.get(url, stream=True)
        self.iter_content = response.iter_content(64)

    def __iter__(self):
        return self

    def __next__(self):
        chunk = next(self.iter_content)
        return chunk

    def download(self, file_path):
        with open(file_path, 'wb') as file:
            for piece in self:
                file.write(piece)


class CountryIterator:

    def __init__(self, file_path):
        self.file_path = file_path
        self.string = -1
        with open(self.file_path) as f:
            self.data = json.load(f)

    def __iter__(self):
        return self

    @simple_logger_decorator
    def __next__(self):

        self.string += 1
        try:
            self.data[self.string]
        except IndexError:
            raise StopIteration
        print(self.data[self.string]['name']['common'])
        country_name = self.data[self.string]['name']['common']
        wiki_country_link = (wiki_link + country_name.replace(' ', '_'))
        return wiki_country_link


class Md5Converter:

    def __init__(self, file_path):
        self.file_path = file_path

    @simple_logger_decorator
    def file_reader(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                md5 = hashlib.md5(line.encode())
                yield md5.hexdigest()


downloader = Downloader(netology_link)
downloader.download('countries.json')

with open('country_links.txt', 'a', encoding="utf-8") as country_links_file:
    for country_link in CountryIterator('countries.json'):
        country_links_file.write(f'{country_link}\n')

output = Md5Converter('country_links.txt')


if __name__ == '__main__':
    for i in output.file_reader():
        print(i)
