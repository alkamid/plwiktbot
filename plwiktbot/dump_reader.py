import bz2
from os import unlink
from tempfile import mkstemp
from typing import Dict, List


from pywikibot.xmlreader import XmlDump, XmlEntry
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


def build_index_dict(index_filename: str) -> Dict[str, List[int]]:
    in_dict = {}
    with bz2.BZ2File(index_filename) as f:
        index_text = f.read().decode('utf-8')

    indices = []
    for i, line in enumerate(index_text.split('\n')):
        lsp = line.split(':', maxsplit=2)
        if not lsp[0]:
            continue
        in_dict[lsp[2]] = [i % 100, int(lsp[0]), None]
        if i % 100 == 0:
            indices.append(int(lsp[0]))

    for i, (key, val) in enumerate(in_dict.items()):
        try:
            in_dict[key][2] = indices[i // 100 + 1]
        except IndexError:
            pass

    return in_dict


def lookup_page(title: str, index_dict: Dict, filename_dump: str) -> XmlEntry:
    id, start, stop = index_dict[title]
    len_header = 670
    with open(filename_dump, 'rb') as f:
        header = f.read(len_header)
        f.seek(start)
        compressed_100_pages = f.read(stop-start)
        try:
            _, tempfile = mkstemp(suffix='.bz2')
            with open(tempfile, 'wb') as g:
                g.write(header + compressed_100_pages)
            gen = XmlDump(tempfile).parse()
            for i, page in enumerate(gen):
                if i == id:
                    return page
        finally:
            unlink(tempfile)

