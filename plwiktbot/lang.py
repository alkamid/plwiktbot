from dataclasses import dataclass, field
import re
from typing import Optional

@dataclass
class Language:
    short_name: str
    code: str
    etym: str
    short_only: bool = False
    jakie: str = None
    zjezyka: str = None
    singular_has_gender: Optional[bool] = None
    plural_has_gender: Optional[bool] = None

    def __post_init__(self):
        # Usually the short name is copied from user-created content
        # on Wiki. To make sure there are no invisible unwanted characters,
        # clean the input first
        clean_word_pattern = re.compile(r'[^\w\s\-\!]+', re.UNICODE)
        self.short_name = clean_word_pattern.sub('', self.short_name)
        self.code = clean_word_pattern.sub('', self.code)
        self.etym = clean_word_pattern.sub('', self.etym)

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