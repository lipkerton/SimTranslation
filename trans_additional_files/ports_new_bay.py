import pickle
from googletrans import Translator
import xml.etree.ElementTree as ET

from methods.constants import (
    project_dir,
    path_dir_for_rus_files,
    path_for_translations,
    files,
)


def printing_translations_into_txt(word, translated_word, file_name):
    file_name.write(word + ';' + translated_word + '\n')


def translate_file_name(line, boss_dict, temporary_dict):

    WORDLIST = sorted(line.split('_'), key=len, reverse=True)

    for WORD in WORDLIST:
        TRANSLATED_WORD = check_the_line_in_dict(
            WORD,
            boss_dict,
            temporary_dict
        )
        line = line.replace(
            WORD,
            TRANSLATED_WORD
        )
    return line


def check_the_line_in_dict(line: str, boss_dict, temporary_dict) -> str:

    MEME_1 = boss_dict.get(line.strip("'"), None)
    MEME_2 = temporary_dict.get(line.strip("'"), None)

    if MEME_1 is None and MEME_2 is None:
        TRANSLATED = translate_line(line.strip("'"))
        temporary_dict[line] = TRANSLATED.strip()
        return TRANSLATED

    if MEME_1 is not None:
        return MEME_1

    return MEME_2


def parse_line(line: str, boss_dict, temporary_dict, file_name) -> str:

    RUS_TEXT = str()
    WORDLIST = list()
    FLAG = False

    for SYMBOL_INDEX in range(len(line) - 1):

        exceptions = ("'", "`")

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
                temporary_dict
            )
            line = line.replace(
                WORD,
                TRANSLATED_WORD
            )
            printing_translations_into_txt(WORD, TRANSLATED_WORD, file_name)
    return line


def match(text: str, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    """Проверка строки на русские символы."""

    if text is not None:
        return not alphabet.isdisjoint(text.lower())
    else:
        return text


def translate_line(line: str) -> str:
    """Перевод строки."""

    result = translator.translate(line, dest='en')
    return result.text


def main():
    file_number = 1  # Переменная, которая показывает номер переведенного файла
    number_translated_lines = 0  # Количество переведенных строк в файле
    temporary_dict = dict()
    saved_dict = open('my_dict.pkl', 'rb')
    boss_dict = pickle.load(saved_dict)
    for file in files:
        if ('.xprt' or 'xml') in file:
            file_name_redacted = file.split('.')[0]
            all_translations_file = open(
                f'{path_for_translations}/{file_name_redacted}.csv', 'w'
            )
            FILE = f'{path_dir_for_rus_files}/{file}'
            NAME_FILE = file
            tree = ET.parse(FILE)
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
                            or 'portnames' in child_name_text
                        ):
                            value_text = child.findtext('value')
                            if value_text is not None:
                                child.find('value').text = parse_line(
                                    value_text,
                                    boss_dict,
                                    temporary_dict,
                                    all_translations_file
                                )
                                number_translated_lines += 1

                    if child.tag == 'plot':
                        title_text = child.findtext('title')
                        if title_text is not None:
                            child.find('title').text = parse_line(
                                title_text,
                                boss_dict,
                                temporary_dict,
                                all_translations_file
                            )
                            number_translated_lines += 1

                    if child.tag == 'bottomaxis':
                        title_text = child.findtext('title')
                        if title_text is not None:
                            child.find('title').text = parse_line(
                                title_text,
                                boss_dict,
                                temporary_dict,
                                all_translations_file
                            )
                            number_translated_lines += 1

                    if child.tag == 'leftaxis':
                        title_text = child.findtext('title')
                        if title_text is not None:
                            child.find('title').text = parse_line(
                                title_text,
                                boss_dict,
                                temporary_dict,
                                all_translations_file
                            )
                            number_translated_lines += 1

                    if child.tag == 'series':
                        title_text = child.findtext('title')
                        if title_text is not None:
                            child.find('title').text = parse_line(
                                title_text,
                                boss_dict,
                                temporary_dict,
                                all_translations_file
                            )
                            number_translated_lines += 1

                    if (
                        child.tag == 'object'
                        and (
                            '102' in child.findtext('obj_type')
                            or '103' in child.findtext('obj_type')
                        )
                    ):
                        for child_child in child.iter('port'):
                            if child_child.tag == 'port':
                                name_text = child_child.findtext('name')
                                if name_text is not None:
                                    child_child.find('name').text = parse_line(
                                        name_text,
                                        boss_dict,
                                        temporary_dict,
                                        all_translations_file
                                    )
                                    number_translated_lines += 1
            translated_file_name = translate_file_name(
                NAME_FILE.split(".")[0],
                boss_dict,
                temporary_dict
            )
            name_file = (
                f'{project_dir}/translated_files/'
                f'{translated_file_name + "_eng"}.xprt'
            )
            all_translations_file.close()
            tree.write(name_file, encoding='utf-8', xml_declaration=True)
            print()
            print(
                f'{NAME_FILE} was translated! File number: {file_number},'
                f'translated lines counter: {number_translated_lines}'
            )
            file_number += 1
            print()
        boss_dict.update(temporary_dict)
    saved_dict.close()
    saved_dict = open('my_dict.pkl', 'wb')
    pickle.dump(boss_dict, saved_dict)
    saved_dict.close()
    print('Files translation has been completed!')


translator = Translator()

main()
