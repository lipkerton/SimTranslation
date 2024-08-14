import pickle
import xml.etree.ElementTree as ET
from pathlib import Path

from .constants import path_for_main_dict_eng, path_for_boss_dict_chn
from .translation_chn_eng import (check_the_line_in_dict, match,
                                  translate_eng_file_name)
from .working_with_files_dirs import (chinese_one_file_exec,
                                      english_one_file_exec,
                                      making_other_files, making_rep)


def parse_line(
        line: str,
        boss_dict: dict,
        file_name: tuple
) -> str:
    """Расшифровка строки."""

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
                boss_dict,
                file_name
            )
            line = line.replace(
                word,
                TRANSLATED_WORD
            )
    return line


def parsing_xml(
        input_file: str, output_folder, input_folder, language
) -> None:

    global FILE_NUMBER
    NUMBER_TRANSLATED_LINES = 0  # Количество переведенных строк в файле

    NAME_FILE = Path(input_file).name.split('.')[0]
    EXTENZ = Path(input_file).suffix

    message = None

    if language.get() == 'English':
        saved_dict = open(path_for_main_dict_eng, 'rb')
        boss_dict = pickle.load(saved_dict)
    else:
        saved_dict = open(path_for_boss_dict_chn, 'rb')
        boss_dict = pickle.load(saved_dict)

    exceptions = ('.xprt', '.xml')

    if EXTENZ not in exceptions:
        making_other_files(input_file, output_folder, input_folder)
    else:
        files_translations = (
            english_one_file_exec(NAME_FILE),
            chinese_one_file_exec(NAME_FILE)
        )

        tree = ET.parse(input_file)
        root_node = tree.getroot()

        # Цикл перебора всех тегов по заданному адресу
        for tag in root_node.findall('project'):
            for child in tag.iter():

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
                                boss_dict,
                                files_translations
                            )
                            NUMBER_TRANSLATED_LINES += 1

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
                            boss_dict,
                            files_translations
                        )
                        NUMBER_TRANSLATED_LINES += 1

            translated_eng_file_name = translate_eng_file_name(
                NAME_FILE,
                boss_dict,
                files_translations
            )

            new_file_path = making_rep(input_file, output_folder, input_folder)
            name_file = (
                f'{new_file_path}/'
                f'{translated_eng_file_name + "_eng"}.xprt'
            )

            files_translations[0].close()
            files_translations[1].close()

            tree.write(name_file, encoding='utf-8', xml_declaration=True)

        message = (
            f'{NAME_FILE} was translated!\nFile number: {FILE_NUMBER}\n'
            f'Translated lines counter: {NUMBER_TRANSLATED_LINES}\n'
            '\n'
        )

        FILE_NUMBER += 1

    saved_dict.close()

    return message


FILE_NUMBER = 1
