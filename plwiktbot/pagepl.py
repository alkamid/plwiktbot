import re
from gettext import find
from typing import Optional, List, Tuple

from pywikibot import Page
from pywikibot import Site
from pywikibot.xmlreader import XmlEntry


class PagePL:
    def __init__(self, parse=True):
        self.site_plwikt = Site('pl', 'wiktionary')
        self.language_sections = dict()
        self.regexps = dict()
        self.header = ''
        if not self.text:
            self.text = ''

        if parse:
            self.find_language_sections()

    def find_language_sections(self):
        header_index = self.text.index('==')
        self.header = self.text[:header_index]

        sec_list = find_sections_seq(self.text[header_index:])
        if sec_list:
            for head, content in sec_list:
                lang_start = head.find('({{') + 3
                lang_end = head.find('}})')
                self.language_sections[head[lang_start:lang_end]] = Section(content)
        else:
            raise SectionsNotFound


class PagePLWiki(Page, PagePL):
    def __init__(self, title, **kwargs):
        site_plwikt = Site('pl', 'wiktionary')
        parse = kwargs.pop('parse', True)
        print(kwargs)
        Page.__init__(self, source=site_plwikt, title=title, **kwargs)
        PagePL.__init__(self, parse=parse)


class PagePLXML(XmlEntry, PagePL):
    def __init__(self, **kwargs):
        PagePL.__init__(self)
        XmlEntry.__init__(self, **kwargs)


class SectionsNotFound(Exception):
    def __init__(self):
        self.value = 'language sections not found!'

    def __str__(self):
        return repr(self.value)


class Section:
    def __init__(self, wikitext: Optional[str]=None, parse=True):
        self.wikitext = wikitext
        self.meanings = ''
        self.senses = list()
        self.pos = list()

        if wikitext is None and parse:
            raise ValueError('In order to parse a section, its wikitext must be provided!')

        if parse:
            self.parse(wikitext)

    def parse(self, wikitext: str) -> None:
        meanings_start = wikitext.find('{{znaczenia}}') + len('{{znaczenia}}')
        meanings_end = wikitext.find('{{odmiana}}')
        self.meanings = wikitext[meanings_start:meanings_end].strip()
        current_pos = None
        for line in self.meanings.split('\n'):
            if line.startswith(': ('):
                assert current_pos is not None
                number_end_idx = line.find(')', 3)
                number = line[3:number_end_idx]
                sense = line[number_end_idx+1:]
                self.senses.append((number, sense, current_pos))
            else:
                current_pos = line
                self.pos.append(current_pos)
        print(self.pos)
        print(self.senses)


def find_sections_seq(text: str) -> List[Tuple[str, str]]:
    sec_list = []

    start = 0
    while start != -1:
        assert text[start:start+2] == '=='
        header_end = text.find('==', start+2)
        header = text[start:header_end+2]
        sec_end = text.find('==', header_end+2)
        if sec_end == -1:
            sec = text[header_end+2:]
        else:
            sec = text[header_end+2:sec_end]
        start = sec_end
        sec_list.append((header, sec))

    return sec_list
