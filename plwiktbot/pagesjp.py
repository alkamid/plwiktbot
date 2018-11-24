from dataclasses import dataclass
from typing import List, Dict, KeysView, Union

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests


class PageSJP:
    def __init__(self, title: str, base_forms_only: bool=True) -> None:
        self.title = title
        self.words = list()
        self.parse_page(base_forms_only)

    def parse_page(self, base_forms_only: bool=True):
        raw_content = requests.get(f'https://sjp.pl/{self.title}').content
        html = BeautifulSoup(raw_content, 'lxml')
        all_words = html.find_all('a', class_='lc')
        if base_forms_only:
            all_words = [w for w in all_words if w.text == self.title]
        for word in all_words:
            self.words.append(WordSJP(word))

    def to_dict(self) -> List[Dict[str, Union[str, Dict[str, List[str]]]]]:
        page_dict = list()
        for word in self.words:
            page_dict.append(word.to_dict())
        return page_dict


class WordSJP:
    def __init__(self, header: Tag) -> None:
        self.title = header.text
        self.flags: Dict[str, List[str]] = dict()
        self.meanings = ''
        self.parse_word(header)

    def parse_word(self, header: Tag) -> None:
        info_table = header.parent.parent.find_next_sibling()
        flag_rows = info_table.find_all('tt')
        for f in flag_rows:
            flag_symbol = f.text
            flag_derivatives = f.parent.parent.find('td').text.split(', ')
            self.flags[flag_symbol] = flag_derivatives
        meaning_contents = info_table.find_next_sibling()
        for i, elem in enumerate(meaning_contents):
            if elem.name == 'br' and i < len(meaning_contents) - 1:
                self.meanings += ' / '
            else:
                try:
                    self.meanings += elem.strip(';, ')
                except TypeError:
                    self.meanings += elem.text

    def get_flags(self) -> KeysView:
        return self.flags.keys()

    def to_dict(self) -> Dict[str, Union[str, Dict[str, List[str]]]]:
        word_dict = dict()
        word_dict['word'] = self.title
        word_dict['flags'] = self.flags
        word_dict['meanings'] = self.meanings
        return word_dict
