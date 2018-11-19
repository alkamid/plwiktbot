from bs4 import BeautifulSoup
from bs4.element import Tag
import requests


class PageSJP:
    def __init__(self, title: str) -> None:
        self.title = title
        self.words = list()
        self.parse_page()

    def parse_page(self):
        raw_content = requests.get(f'https://sjp.pl/{self.title}').content
        html = BeautifulSoup(raw_content, 'lxml')
        all_words = html.find_all('a', class_='lc')
        for word in all_words:
            self.words.append(WordSJP(word))


class WordSJP:
    def __init__(self, header) -> None:
        self.title = header.text
        self.flags = list()
        self.inflections = list()
        self.meanings = ''
        self.parse_word(header)

    def parse_word(self, header: Tag) -> None:
        info_table = header.parent.parent.find_next_sibling()
        meaning_text = info_table.find_next_sibling()
        print(meaning_text)

