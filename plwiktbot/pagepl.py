from typing import Optional, List, Tuple, Union, Dict

from pywikibot import Page
from pywikibot import Site
from pywikibot.xmlreader import XmlEntry

from plwiktbot.lang import Sense, POS


class PagePL:
    def __init__(self, parse=True, languages: Optional[Union[str, List[str]]] = None):
        self.site_plwikt = Site('pl', 'wiktionary')
        self.language_sections: Dict[str, Section] = dict()
        self.header = ''
        try:
            assert isinstance(self.text, str)
        except AttributeError:
            self.text = ''

        if parse:
            self.parse(languages)

    def parse(self, languages: Optional[Union[str, List[str]]] = None):
        self.find_language_sections(languages)

    def find_language_sections(self, languages: Optional[Union[str, List[str]]]=None):
        header_index = self.text.index('==')
        self.header = self.text[:header_index]

        if isinstance(languages, str):
            languages = [languages]

        sec_list = find_sections_seq(self.text[header_index:])
        if languages is not None:
            sec_list = [s for s in sec_list if any(l in s[0] for l in languages)]
        if sec_list:
            for head, content in sec_list:
                lang_start = head.find('({{') + 3
                lang_end = head.find('}})')
                self.language_sections[head[lang_start:lang_end]] = Section(content)
        elif languages is None:
            raise SectionsNotFound


class PagePLWiki(Page, PagePL):
    def __init__(self, title: str, **kwargs):
        site_plwikt = Site('pl', 'wiktionary')
        parse = kwargs.pop('parse', True)
        Page.__init__(self, source=site_plwikt, title=title, **kwargs)
        PagePL.__init__(self, parse=parse)


class PagePLXML(PagePL):
    def __init__(self, xmlentry: XmlEntry, **kwargs):
        self.__dict__.update(xmlentry.__dict__)
        if int(self.ns) == 0 and not self.isredirect and not self.title.startswith('Słownik '):
            PagePL.__init__(self, **kwargs)
        else:
            kwargs.pop('parse', True)
            PagePL.__init__(self, parse=False, **kwargs)


class SectionsNotFound(Exception):
    def __init__(self):
        self.value = 'language sections not found!'

    def __str__(self):
        return repr(self.value)


class Section:
    def __init__(self, wikitext: Optional[str]=None, parse=True):
        self.wikitext = wikitext
        self.meanings = ''
        self.senses: List[Sense] = list()
        self.pos: List[POS] = list()

        if wikitext is None and parse:
            raise ValueError('In order to parse a section, its wikitext must be provided!')
        elif wikitext is not None and parse:
            self.parse(wikitext)

    def parse(self, wikitext: str) -> None:
        meanings_start = wikitext.find('{{znaczenia}}') + len('{{znaczenia}}')
        meanings_end = wikitext.find('{{odmiana}}')
        self.meanings = wikitext[meanings_start:meanings_end].strip()
        current_pos = POS('')
        for line in self.meanings.split('\n'):
            if not line.startswith(': ('):
                current_pos = POS(line)
                self.pos.append(current_pos)
            else:
                number_end_idx = line.find(')', 3)
                number = line[3:number_end_idx]
                sense = line[number_end_idx+1:].strip()
                self.senses.append(Sense(number, sense, current_pos))


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
