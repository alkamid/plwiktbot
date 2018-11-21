import json
from typing import Dict, Optional, List

from plwiktbot.pagesjp import PageSJP


def get_words_from_sjp(wordlist: List[str]) -> Dict:
    output_dict = dict()
    for word in wordlist:
        page = PageSJP(word)
        output_dict[word] = page.to_dict()

    return output_dict


def save_words_to_json(word_dict: Dict, output_file: str, file_to_append: Optional[str]) -> None:
    try:
        with open(file_to_append) as f:
            existing_dict = json.load(f)
    except FileNotFoundError:
        existing_dict = dict()

    existing_dict.update(word_dict)
    with open(output_file, 'w') as f:
        json.dump(existing_dict, f, ensure_ascii=False)



