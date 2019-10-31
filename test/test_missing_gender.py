from plwiktbot.pagepl import PagePLWiki


def test_missing_gender():
    test_page = PagePLWiki(title='ווינטפּאָקן', parse=False)  # Yiddish plurale tantum
    test_page.text = test_page.getOldVersion(oldid=7022010)
    test_page.parse(['jidysz'])
    assert test_page.language_sections['jidysz'].pos[0].has_valid_gender()

    # French should have gender but doesn't
    # Polish should have gender and does
    test_page = PagePLWiki(title='hetman', parse=False)
    test_page.text = test_page.getOldVersion(oldid=6758705)
    test_page.parse(['francuski', 'polski'])
    assert not test_page.language_sections['francuski'].pos[0].has_valid_gender()

    assert all(p.has_valid_gender() for p in test_page.language_sections['polski'].pos)

    test_page = PagePLWiki(title='sanki', parse=False)  # Polish plurale tantum
    test_page.text = test_page.getOldVersion(oldid=6354030)
    test_page.parse(['polski'])
    assert test_page.language_sections['polski'].pos[0].has_valid_gender()


