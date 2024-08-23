import xml.etree.ElementTree as ET

from .working_with_files_dirs import making_rep
from .constants import iter_tags
from .classes import LineTranslate


def translate_file_name(
        file_name: str,
        CORE_SETTINGS
) -> str:
    """Translating file name."""
    line_obj = LineTranslate(file_name, CORE_SETTINGS)
    return line_obj.words_in_line_translate(file_name)


def searching_tag(
        child,
        CORE_SETTINGS
) -> None:
    """Asking which tag we recieved
    if it is 'data' or 'plot', 'bottomaxis', 'leftaxis', 'series'
    we translate contents of tags 'value' or 'title'."""
    if child.tag == 'data':
        child_name_text = child.findtext('name').lower()
        if (
            'labeltext' in child_name_text
            or 'text' in child_name_text
            or 'caption' in child_name_text
        ):
            value_text = child.findtext('value')
            if value_text is not None:
                value_obj = LineTranslate(value_text, CORE_SETTINGS)
                if value_obj.translator_flag:
                    value_obj.core_parse_line()
                    result = value_obj.words_in_line_translate()
                    value_obj.CORE_SETTINGS.upd_lines_counter()
                    child.find('value').text = result
    if child.tag in iter_tags:
        title_text = child.findtext('title')
        if title_text is not None:
            title_obj = LineTranslate(title_text, CORE_SETTINGS)
            if title_obj.translator_flag:
                title_obj.core_parse_line()
                result = title_obj.words_in_line_translate()
                title_obj.CORE_SETTINGS.upd_lines_counter()
                child.find('title').text = result


def parsing_xml(
        CORE_SETTINGS
) -> str:
    """Parsing xml and choosing tags which we need to translate,
    tags what we are going to translate - 'value', 'title'."""
    CORE_SETTINGS.upd_lines_counter(zeroed=True)
    tree = ET.parse(CORE_SETTINGS.input_file)
    root_node = tree.getroot()
    for tag in root_node.findall('project'):
        for child in tag.iter():
            searching_tag(child, CORE_SETTINGS)
    translated_file_name = translate_file_name(
        CORE_SETTINGS.name_file,
        CORE_SETTINGS
    ).replace(' ', '_')
    new_file_path = making_rep(
        CORE_SETTINGS
    )
    name_file = (
        f'{new_file_path}/'
        f'{translated_file_name}_'
        f'{CORE_SETTINGS.abs_for_translator}.xprt'
    )
    tree.write(name_file, encoding='utf-8', xml_declaration=True)
    CORE_SETTINGS.files_translations.close()
    CORE_SETTINGS.upd_files_counter()
    return CORE_SETTINGS.compile_message()
