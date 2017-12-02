from ..pagepl import PagePLWiki


def test_meanings():
    test_page = PagePLWiki(title='robić')
    test_page.text = test_page.getOldVersion(oldid=5125503)
    assert test_page.title() == 'robić'

    # assert len(test_page.language_sections) == 1
    # assert test_page.language_sections['polski'].subsections['przykłady'][0].text == \
    #     '\'\'[[w|W]] [[ten|tej]] [[fabryka|fabryce]] [[robić|robią]] [[samochód|samochody]].\'\''
    # assert test_page.language_sections['polski'].subsections['przykłady'][1].number == '(1.1)'
