import pickle
import xml.etree.ElementTree as ET

from .constants import path_for_main_dict, path_for_translations_eng
from .translation_chn_eng import (check_the_line_in_dict, match,
                                  translate_file_name)
from .working_with_files_dirs import (chinese_unpacking, making_other_files,
                                      making_rep)


def parse_line(
        line: str,
        boss_dict: dict,
        temporary_dict: dict,
        file_name: str
) -> str:
    """Расшифровка строки."""

    RUS_TEXT = str()  # Создаем новую строку.
    WORDLIST = list()  # Создаем пустой список.
    FLAG = False

    for SYMBOL_INDEX in range(len(line) - 1):

        exceptions = ("'", "`", '"')

        if FLAG:
            RUS_TEXT += line[SYMBOL_INDEX]

        if line[SYMBOL_INDEX] in exceptions:
            FLAG = True

        if line[SYMBOL_INDEX + 1] in exceptions:
            WORDLIST.append(RUS_TEXT.strip())
            RUS_TEXT = str()
            FLAG = False

    WORDLIST = sorted(WORDLIST, key=len, reverse=True)

    for WORD in WORDLIST:
        if match(WORD):
            TRANSLATED_WORD = check_the_line_in_dict(
                WORD,
                boss_dict,
                temporary_dict,
                file_name
            )
            line = line.replace(
                WORD,
                TRANSLATED_WORD
            )
    return line


def parsing_xml(
        file: str
) -> None:
    FILE_NUMBER = 1  # Переменная, которая показывает номер переведенного файла
    NUMBER_TRANSLATED_LINES = 0  # Количество переведенных строк в файле
    # NAME_FILE = file[file.rfind('/') + 1:].split('.')[-2]  # macOS version
    NAME_FILE = file[file.rfind('\\') + 1:].split('.')[-2]  # win version
    # EXTENZ = file[file.rfind('/') + 1:].split('.')[-1]
    EXTENZ = file[file.rfind('\\') + 1:].split('.')[-1]
    saved_dict = open(path_for_main_dict, 'rb')
    boss_dict = pickle.load(saved_dict)
    exceptions = ('xprt', 'prt', 'xml')
    if EXTENZ not in exceptions:
        making_other_files(file)
    else:
        temporary_dict = dict()
        all_translations_file = open(
            f'{path_for_translations_eng}/{NAME_FILE}.csv', 'w', encoding='utf-8'
        )
        tree = ET.parse(file)
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
                                temporary_dict,
                                all_translations_file
                            )
                            NUMBER_TRANSLATED_LINES += 1

                if child.tag == 'plot':
                    title_text = child.findtext('title')
                    if title_text is not None:
                        child.find('title').text = parse_line(
                            title_text,
                            boss_dict,
                            temporary_dict,
                            all_translations_file
                        )
                        NUMBER_TRANSLATED_LINES += 1

                if child.tag == 'bottomaxis':
                    title_text = child.findtext('title')
                    if title_text is not None:
                        child.find('title').text = parse_line(
                            title_text,
                            boss_dict,
                            temporary_dict,
                            all_translations_file
                        )
                        NUMBER_TRANSLATED_LINES += 1

                if child.tag == 'leftaxis':
                    title_text = child.findtext('title')
                    if title_text is not None:
                        child.find('title').text = parse_line(
                            title_text,
                            boss_dict,
                            temporary_dict,
                            all_translations_file
                        )
                        NUMBER_TRANSLATED_LINES += 1

                if child.tag == 'series':
                    title_text = child.findtext('title')
                    if title_text is not None:
                        child.find('title').text = parse_line(
                            title_text,
                            boss_dict,
                            temporary_dict,
                            all_translations_file
                        )
                        NUMBER_TRANSLATED_LINES += 1
            translated_file_name = translate_file_name(
                NAME_FILE,
                boss_dict,
                temporary_dict,
                all_translations_file
            )
            new_file_path = making_rep(file)
            name_file = (
                f'{new_file_path}/'
                f'{translated_file_name + "_eng"}.xprt'
            )
            all_translations_file.close()
            tree.write(name_file, encoding='utf-8', xml_declaration=True)
            print()
            print(
                f'{NAME_FILE} was translated! File number: {FILE_NUMBER},'
                f'translated lines counter: {NUMBER_TRANSLATED_LINES}'
            )
            FILE_NUMBER += 1
            print()
            boss_dict.update(temporary_dict)
    saved_dict.close()
    saved_dict = open(path_for_main_dict, 'wb')
    pickle.dump(boss_dict, saved_dict)
    saved_dict.close()
    chinese_unpacking()
    print('Files translation has been completed!')
