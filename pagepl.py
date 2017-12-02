from pywikibot import Page
from pywikibot import Site
from pywikibot.xmlreader import XmlEntry


class PagePL:
    def __init__(self):
        self.site_plwikt = Site('pl', 'wiktionary')
        self.language_sections = None


class PagePLWiki(Page, PagePL):
    def __init__(self, title, **kwargs):
        PagePL.__init__(self)
        Page.__init__(self, source=self.site_plwikt, title=title, **kwargs)


class PagePLXML(XmlEntry, PagePL):
    def __init__(self, title, **kwargs):
        PagePL.__init__(self)
        XmlEntry.__init__(self, **kwargs)