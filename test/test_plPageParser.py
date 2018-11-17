from plwiktbot.pagepl import PagePLWiki


def test_meanings():
    test_page = PagePLWiki(title='robić', parse=False)
    test_page.text = test_page.getOldVersion(oldid=6202869)
    assert test_page.title() == 'robić'
    test_page.find_language_sections()

    assert len(test_page.language_sections) == 1
    plsec = test_page.language_sections['język polski']

    assert 'czasownik przechodni niedokonany' in plsec.pos[0].wikitext
    assert plsec.pos[0].pos_class == 'verb'
    assert plsec.senses[0].id == '1.1'
    assert plsec.senses[0].wikitext == '[[wykonywać]] [[coś]], [[tworzyć]], [[produkować]], [[przyrządzać]], [[przygotowywać]]'
    assert plsec.senses[0].pos == plsec.pos[0]

    assert plsec.pos[2].pos_class == 'verb'
    assert plsec.senses[6].id == '3.2'
    assert plsec.senses[6].wikitext == '[[stawać się]] [[jakiś|jakimś]], [[zmieniać się]]<ref name="SJPonline-się" />'
    assert plsec.senses[6].pos == plsec.pos[2]
