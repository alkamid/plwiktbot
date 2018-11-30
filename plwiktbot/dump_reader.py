import json
import bz2
import os
from tempfile import mkstemp
from typing import Dict, List, Optional, Tuple


from pywikibot.xmlreader import XmlDump, XmlEntry
from plwiktbot.pagepl import PagePLXML
from plwiktbot.tools import dewikify


def build_dictionary(dump_filename: str, output_filename: Optional[str]=None) -> Dict[str, str]:
    page_generator = XmlDump(dump_filename).parse()
    dictionary = dict()
    for p in page_generator:
        try:
            page = PagePLXML(p, languages=['polski'])
            plsec = page.language_sections['język polski']
        except KeyError:
            continue
        except ValueError as e:
            raise e
        if ' ' in page.title or '-' in page.title or page.title[0].isupper():
            continue
        entry = '; '.join([dewikify(s.wikitext, remove_templates=True)
                           for s in plsec.senses])
        dictionary[page.title] = entry

    if output_filename is not None:
        with open(output_filename, 'w') as f:
            json.dump(dictionary, f, ensure_ascii=False)

    return dictionary


def read_dump(filename: str):
    page_generator = XmlDump(filename).parse()
    for p in page_generator:
        try:
            page = PagePLXML(p, languages=['polski'])
        except ValueError as e:
            raise e
        try:
            print([dewikify(s.wikitext, remove_templates=True)
                   for s in page.language_sections['język polski'].senses])
        except KeyError:
            pass


def build_multistream_index_dict(index_filename: str) -> Dict[str, Tuple[int, int, int]]:
    """
    Take a multistream index file and build a look-up dictionary for each page.
    Args:
        index_filename:
    Returns:
        Dict of page -> (page id in a chunk, starting byte of the chunk, ending byte of the chunk)
        The last element of the tuple is -1 for the last chunk of bzipped multistream dump.
    """
    index_dict = {}
    indices = []
    with bz2.open(index_filename, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            lsp = line.split(':', maxsplit=2)
            start_index = lsp[0]
            if not start_index:
                continue
            page_title = lsp[2].strip()
            index_dict[page_title] = (i % 100, int(start_index), -1)
            if i % 100 == 0:
                indices.append(int(start_index))

    for i, (key, val) in enumerate(index_dict.items()):
        try:
            index_dict[key] = (*index_dict[key][:2], indices[i // 100 + 1])
        except IndexError:
            pass

    return index_dict


def lookup_page(title: str, filename_dump: str, index_dict: Optional[Dict]=None) -> XmlEntry:
    """
    Look up a page in a multistream dump. If the page index is loaded into memory and given as
    index_dict, this function returns a page with a given title from an XML dump in a matter of 10-30ms.
    Args:
        title: Title of the page to be looked up
        filename_dump:
        index_dict: Optional, but recommended. A pre-build index of where particular titles are in
        the multistream dump. If not given, we'll try to do a naive search for the proper file.

    Returns:
        XmlEntry of the desired page
    """
    if index_dict is None:
        print('Looking up the index file... (for better performance, build the index dictionary first,'
              ' and then look up pages)')
        index_path = str(filename_dump).replace('.xml.bz2', '-index.txt.bz2')
        try:
            index_dict = build_multistream_index_dict(index_path)
        except FileNotFoundError:
            raise FileNotFoundError(f'Automatic lookup of the index file failed!\nFile not found: {index_path}\n'
                                    'Make sure the index is in the same directory as dump or provide an already'
                                    'built index mapping as the third argument to lookup_page()')  # TODO: replace lookup_page() with auto generated name of the function

    id_, start, stop = index_dict[title]
    len_header = list(index_dict.values())[0][1]  # the first element in the dict starts at the "header" of "offset"
    with open(filename_dump, 'rb') as f:
        header = f.read(len_header)
        f.seek(start)
        if stop != -1:
            compressed_100_pages = f.read(stop-start)
        else:
            compressed_100_pages = f.read()
        tempfile_handle, tempfile = mkstemp(suffix='.bz2')
        try:
            with open(tempfile, 'wb') as g:
                g.write(header + compressed_100_pages)
            gen = XmlDump(tempfile).parse()
            for i, page in enumerate(gen):
                if i == id_:
                    return page
        finally:
            os.close(tempfile_handle)
            os.unlink(tempfile)


