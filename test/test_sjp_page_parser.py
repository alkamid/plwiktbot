import json
from plwiktbot import pagesjp


def test_getting_meanings():
    p = pagesjp.PageSJP('fok')
    for word in p.words:
        if word.title == 'fok':
            fok = word
            flags = fok.get_flags()
            assert tuple(flags) == ('N', 'O', 'T', 's')

        if word.title == 'foki':
            foki = word
            assert foki.meanings == '1. skórzane lub aksamitne pasy podpinane pod narty dla ułatwienia wejścia na strome zbocze / 2. futro ze skór fok lub kotików'
