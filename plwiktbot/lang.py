from dataclasses import dataclass, field
import re
from typing import Optional

import pywikibot

# TODO: auto "etym" discovery
# TODO: don't hardcode
LANG_ADJECTIVES = {'białoruski (taraszkiewica)': {'jakie': 'białoruskie (taraszkiewica)', 'zjezyka': 'białoruskiego (taraszkiewicy)'},
                   'norweski (bokmål)': {'jakie': 'norweskie (bokmål)', 'zjezyka': 'norweskiego (bokmål)'},
                   'norweski (nynorsk)': {'jakie': 'norweskie (nynorsk)', 'zjezyka': 'norweskiego (nynorsk)'},
                   'norweski (riksmål)': {'jakie': 'norweskie (riksmål)', 'zjezyka': 'norweskiego (riksmål)'},
                   'esperanto (morfem)': {'jakie': 'esperanto (morfem)', 'zjezyka': 'esperanto (morfem)'},
                   'chantyjski (szurykszarski)': {'jakie': 'chantyjskie (szurykszarskie)', 'zjezyka': 'chantyjskiego (szurykszarskiego)'},
                   'chantyjski (kazymski)': {'jakie': 'chantyjskie (kazymskie)', 'zjezyka': 'chantyjskiego (kazymskiego)'},
                   'chantyjski (surgucki)': {'jakie': 'chantyjskie (surguckiego)', 'zjezyka': 'chantyjskiego (surguckiego)'},
                   'chantyjski (wachowski)': {'jakie': 'chantyjskie (wachowskie)', 'zjezyka': 'chantyjskiego (wachowskiego)'}}


class LanguageError(Exception):
    pass


@dataclass
class Language:
    short_name: str
    code: Optional[str] = None
    etym: Optional[str] = None
    short_only: bool = False
    jakie: Optional[str] = None
    zjezyka: Optional[str] = None
    singular_has_gender: Optional[bool] = None
    plural_has_gender: Optional[bool] = None

    def __post_init__(self):
        # Usually the short name is copied from user-created content
        # on Wiki. To make sure there are no invisible unwanted characters,
        # clean the input first
        clean_word_pattern = re.compile(r'[^\w\s\-\!\(\)]+', re.UNICODE)
        self.short_name = clean_word_pattern.sub('', self.short_name)
        if self.code is not None:
            self.code = clean_word_pattern.sub('', self.code)
        if self.etym is not None:
            self.etym = clean_word_pattern.sub('', self.etym)

        if self.jakie is None:
            try:
                self.jakie = LANG_ADJECTIVES[self.short_name]['jakie']
            except KeyError:
                pass
        if self.zjezyka is None:
            try:
                self.zjezyka = LANG_ADJECTIVES[self.short_name]['zjezyka']
            except KeyError:
                pass

        if '(' in self.short_name and (self.jakie is None or self.zjezyka is None):
            raise ValueError(f'Language name ({self.short_name}) too complicated for automatic adjective discovery!'
                             f' Provide "jakie" and "zjezyka" parameters.')

        if self.short_name.endswith('ski'):
            self.jakie = self.jakie or self.short_name + 'e'
            self.zjezyka = self.zjezyka or self.short_name + 'ego'
        else:
            self.jakie = self.jakie or self.short_name
            self.zjezyka = self.zjezyka or self.short_name

        
@dataclass
class POS:
    wikitext: str
    lang: Optional[Language] = None
    pos_class: str = field(init=False)

    def __post_init__(self):
        self.pos_class = self.parse_pos()

    def parse_pos(self) -> str:
        text = self.wikitext.strip("'\n")
        if text == '':
            pos = 'None'
        elif 'rzeczownik' in text:
            pos = 'noun'
        elif 'czasownik' in text:
            pos = 'verb'
        elif 'przymiotnik' in text:
            pos = 'adjective'
        elif 'przysłówek' in text:
            pos = 'adverb'
        elif 'spójnik' in text:
            pos = 'conjunction'
        elif 'zaimek' in text:
            pos = 'pronoun'
        elif 'przyimek' in text:
            pos = 'preposition'
        elif 'wykrzyknik' in text:
            pos = 'interjection'
        elif 'partykuła' in text:
            pos = 'particle'
        elif 'liczebnik' in text:
            pos = 'numeral'
        else:
            pos = 'other'
        return pos

    def has_valid_gender(self):
        if self.pos_class != 'noun':
            raise NotImplementedError('Gender checking is only implemented for nouns!')
        else:
            if '{{forma rzeczownika' in self.wikitext:
                return True
            else:
                if 'liczba mnoga' in self.wikitext and self.lang.plural_has_gender is False:
                    return True
                elif 'liczba mnoga' in self.wikitext and 'rodzaj' not in self.wikitext:
                    return False
                elif 'rodzaj' not in self.wikitext and self.lang.singular_has_gender:
                    return False
                else:
                    return True


@dataclass
class Sense:
    id: str
    wikitext: str
    pos: POS


def get_all_languages():
    site = pywikibot.Site('pl', 'wiktionary')
    lang_page = pywikibot.Page(site, 'Mediawiki:Gadget-langdata.js').get()

    lang_table = {}
    re_langs_section = re.compile(r'lang2code: {\n(.*?)\n\t},', re.DOTALL)
    re_one_lang = re.compile(r'\s*?\"(.*?)\"\s*?:\s*\"([a-z-]*?)\"')
    re_short_langs_section = re.compile(r'shortLangs: \[\n(.*?)\n\t\]', re.DOTALL)
    re_one_short_lang = re.compile(r'\s*?\"(.*?)\"(?:,\s*|\n)?')

    s_langs = re.search(re_langs_section, lang_page)
    s_shorts = re.search(re_short_langs_section, lang_page)

    gender_page = pywikibot.Page(site, 'User:AlkamidBot/listy/rodzaj/wykluczone').get()
    gender_lines = gender_page.split('\n')[2:]  # ignore the header
    without_gender = [line.strip() for line in gender_lines if len(line) > 1]

    # TODO: don't hardcode, put on wiki
    no_gender_in_plural = ['jidysz', 'niemiecki']

    all_langs = re.findall(re_one_lang, s_langs.group(1))
    all_short = re.findall(re_one_short_lang, s_shorts.group(1))
    for short_name, code in all_langs:
        short_only = True if short_name in all_short else False
        plu_has_gender = True
        sing_has_gender = True
        if short_name in without_gender:
            sing_has_gender = False
            plu_has_gender = False

        if short_name in no_gender_in_plural:
            plu_has_gender = False

        lang_table[short_name] = Language(short_name, code, short_only=short_only,
                                          singular_has_gender=sing_has_gender,
                                          plural_has_gender=plu_has_gender)

    return lang_table
