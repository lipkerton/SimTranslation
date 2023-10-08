import xml.etree.ElementTree as ET
import pathlib
import os
from googletrans import Translator


translator = Translator()
KEY_WORDS = dict()
project_dir = str(pathlib.Path.cwd())
dir_path = str(pathlib.Path.cwd()) + '/files_for_translate'
files = os.listdir(dir_path)
file_number = 1
number_translated_lines = 0


def check_length_line(line):
    """Подготовка и отправка строки на перевод."""
    if line not in KEY_WORDS.keys():
        lines = line.split("'")
        for i in range(len(lines)):
            if match(lines[i]):
                lines[i] = translate_line(lines[i])
        lines = "'".join(lines)
        KEY_WORDS[line] = lines
        return lines
    else:
        return KEY_WORDS[line]


def translate_line(line):
    """Перевод строки."""
    result = translator.translate(line, dest='en')
    return result.text


def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    """Проверка строки на русские символы."""
    if text is not None:
        return not alphabet.isdisjoint(text.lower())
    else:
        return text


for file in files:
    if ('.xprt' or 'xml') in file:
        FILE = f'{dir_path}/{file}'
        NAME_FILE = file
        tree = ET.parse(FILE)
        root_node = tree.getroot()
        for tag in root_node.findall('project/page/object'):
            for child in tag.iter():
                if match(child.text) and child.tag == 'value' and '#13#10' in child.text:
                    child.text = check_length_line(child.text)
                    number_translated_lines += 1
                    print(child.text)
        name_file = f'{project_dir}/translated_files/{NAME_FILE.split(".")[0] + "_eng"}.xml'
        tree.write(name_file, encoding='utf-8', xml_declaration=True)
        print()
        print(f'{NAME_FILE} was translated! File number: {file_number}, translated lines counter: {number_translated_lines}')
        file_number += 1
        print()
    else:
        continue
print('Files translation has been completed!')
