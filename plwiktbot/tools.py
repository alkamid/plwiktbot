import re


def dewikify(input_text: str,
             remove_refs: bool=True,
             remove_templates: bool=True,
             expand_templates: bool=False) -> str:
    """
    Dewikify a wikified string.
    Args:
        input_text (str): wikified text ([[word]]s [[be|are]] [[write|written]]
            [[like]] [[this]])
        remove_refs (bool): if True (default), remove <ref> tags and their contents
        remove_templates (bool): if False (default), don't remove templates
        expand_templates (bool): if False (default), don't expand templates
    Returns:
        str: unwikified text (words are written like this)
    """

    if remove_refs:
        re_refs = re.compile(r'<ref.*?(?:/>|</ref>)')
        input_text = re.sub(re_refs, '', input_text)

    if remove_templates:
        if expand_templates:
            raise AttributeError('Templates cannot be expanded if remove_templates==True!')
        re_templates = re.compile(r'({{.*?}})')
        input_text = re.sub(re_templates, '', input_text)

    # https://regex101.com/r/yB0pZ6/1
    re_base_form = re.compile(r'(\[\[(?:[^\]\|]*?\||)(.*?)\]\])')
    dewikified = re.sub(re_base_form, r'\2', input_text)
    return dewikified.strip()
