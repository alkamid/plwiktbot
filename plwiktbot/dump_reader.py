from pywikibot.xmlreader import XmlDump
from plwiktbot.pagepl import PagePLXML


def read_dump(filename: str):
    page_generator = XmlDump(filename).parse()
    i = 0
    for p in page_generator:
        try:
            page = PagePLXML(p, languages=['polski'])
        except ValueError as e:
            raise e
        try:
            print(page.language_sections['język polski'].meanings)
        except KeyError:
            pass


