import re
from pywikibot import Page
from pywikibot import Site
from pywikibot.xmlreader import XmlEntry


class PagePL:
    def __init__(self, parse=True):
        self.site_plwikt = Site('pl', 'wiktionary')
        self.language_sections = dict()
        self.regexps = dict()
        self.regexps['header'] = re.compile(r'(.*?)==', re.DOTALL)
        self.regexps['lang_section'] = re.compile(r'(== .*?\(\{\{.*?\}\}\) ==.*?)(?=$|[^{{]==)', re.DOTALL)

        if parse:
            self.find_language_sections()

    def find_language_sections(self):
        s_header = re.search(self.regexps['header'], self.text)
        if s_header:
            self.language_sections['header'] = s_header.group(1)

        s_lang = re.findall(self.regexps['lang_section'], self.text)
        if s_lang:
            tempidx = 'abcdefg'
            for i, l in enumerate(s_lang):
                self.language_sections[tempidx[i]] = l
                #self.listLangs.append(LanguageSection(l, self.title))
        else:
            raise SectionsNotFound


class PagePLWiki(Page, PagePL):
    def __init__(self, title, **kwargs):
        site_plwikt = Site('pl', 'wiktionary')
        Page.__init__(self, source=site_plwikt, title=title, **kwargs)
        PagePL.__init__(self)


class PagePLXML(XmlEntry, PagePL):
    def __init__(self, **kwargs):
        PagePL.__init__(self)
        XmlEntry.__init__(self, **kwargs)


class SectionsNotFound(Exception):
    def __init__(self):
        self.value = 'language sections not found!'

    def __str__(self):
        return repr(self.value)
