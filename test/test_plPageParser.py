from plwiktbot.pagepl import PagePLWiki


def test_meanings():
    test_page = PagePLWiki(title='robić')
    test_page.text = test_page.getOldVersion(oldid=6202869)
    assert test_page.title() == 'robić'

    assert len(test_page.language_sections) == 2
    plsec = test_page.language_sections['polski']
    plsec.parse()

    assert plsec.pos[0] == 'czasownik przechodni niedokonany'
    assert plsec.sense[0].id == '1.1'
    assert plsec.sense[0].wikitext == '[[wykonywać]] [[coś]], [[tworzyć]], [[produkować]], [[przyrządzać]], [[przygotowywać]]'
    assert plsec.sense[0].pos == plsec.pos[0]

    assert plsec.sense[6].id == '3.2'
    assert plsec.sense[6].wikitext == '[[stawać się]] [[jakiś|jakimś]], [[zmieniać się]]<ref name="SJPonline-się" />'
    assert plsec.sense[6].pos == plsec.pos[2]
