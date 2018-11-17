from dataclasses import dataclass, field


@dataclass
class POS:
    wikitext: str
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


@dataclass
class Sense:
    id: str
    wikitext: str
    pos: POS
