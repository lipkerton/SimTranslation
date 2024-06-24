from googletrans import Translator
from dictionary import sample_of_starting_dict
from constants import path_for_translations_chn


translator = Translator()


def translate_line_chn(
        line: str
) -> str:
    result = translator.translate(line, dest='zh-cn')
    return result.text


def file_making():
    with open(
        f'{path_for_translations_chn}/chn_base_dictionary.csv', 'a',
        encoding='utf-8'
    ) as chn:
        for key, value in sample_of_starting_dict.items():
            chn.write(
                f'{key.strip()};{value};{translate_line_chn(value.strip())}\n'
            )


file_making()
