import xml.etree.ElementTree as ET

from .translation_chn_eng import (check_the_line_in_dict,
                                  match,
                                  translate_file_name)
from .working_with_files_dirs import making_rep


def parse_line(
        line: str,
        obj_sample
) -> str:
    """Decoding line. So, i'm choosing only words in quotes,
    couse it's the only way to parse the line without ruining main
    logic. Words in quotes are going into the wordlist and
    in next check-in procedures."""
    RUS_TEXT = str()
    WORDLIST = list()
    FLAG = False
    for symbol_index in range(len(line) - 1):
        exceptions = ("'", "`", '"')
        if FLAG:
            RUS_TEXT += line[symbol_index]
        if line[symbol_index] in exceptions:
            FLAG = True
        if line[symbol_index + 1] in exceptions:
            WORDLIST.append(RUS_TEXT.strip())
            RUS_TEXT = str()
            FLAG = False
    WORDLIST = sorted(WORDLIST, key=len, reverse=True)
    for word in WORDLIST:
        if match(word):
            TRANSLATED_WORD = check_the_line_in_dict(
                word,
                obj_sample
            )
            line = line.replace(
                word,
                TRANSLATED_WORD
            )
    return line


def searching_tag(child, obj_sample):
    if child.tag == 'data':
        child_name_text = child.findtext('name').lower()
        if (
            'labeltext' in child_name_text
            or 'text' in child_name_text
            or 'caption' in child_name_text
        ):
            value_text = child.findtext('value')
            if value_text is not None:
                child.find('value').text = parse_line(
                    value_text,
                    obj_sample
                )
                obj_sample.upd_lines_counter()
    if (
        child.tag == 'plot'
        or child.tag == 'bottomaxis'
        or child.tag == 'leftaxis'
        or child.tag == 'series'
    ):
        title_text = child.findtext('title')
        if title_text is not None:
            child.find('title').text = parse_line(
                title_text,
                obj_sample
            )
            obj_sample.upd_lines_counter()


def parsing_xml(
        obj_sample
) -> str:
    """Parsing xml and choosing tags which we need to translate,
    tags what we are going to translate - 'value', 'title'."""
    obj_sample.upd_lines_counter(zeroed=True)
    tree = ET.parse(obj_sample.input_file)
    root_node = tree.getroot()
    for tag in root_node.findall('project'):
        for child in tag.iter():
            searching_tag(child, obj_sample)
        translated_file_name = translate_file_name(
            obj_sample
        )
        new_file_path = making_rep(
            obj_sample
        )
        name_file = (
            f'{new_file_path}/'
            f'{translated_file_name}_'
            f'{obj_sample.abs_for_translator}.xprt'
        )
        obj_sample.files_translations.close()
        tree.write(name_file, encoding='utf-8', xml_declaration=True)
    obj_sample.upd_files_counter()
    message = (
        f'{obj_sample.name_file} was translated!\n'
        f'File number: {obj_sample.num_files}\n'
        f'Translated lines counter: {obj_sample.num_lines}\n'
        '\n'
    )
    return message
