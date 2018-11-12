from typing import Optional


class POS:
    def __init__(self, wikitext: Optional[str]=None):
        if wikitext is not None:
            self.parse(wikitext)
        self.wikitext = None

    def parse(self, wikitext: str):
        pass
