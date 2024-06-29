from googletrans import Translator
import pickle
from constants import path_for_translations_chn, path_for_main_dict


translator = Translator()
saved_dict = open(path_for_main_dict, 'rb')
boss_dict = pickle.load(saved_dict)


def translate_line_chn(
        line: str
) -> str:
    """Translating chinese line."""
    result = translator.translate(line, dest='zh-cn')
    return result.text


def file_making() -> None:
    with open(
        f'{path_for_translations_chn}/chn_base_dictionary.csv', 'a',
        encoding='utf-8'
    ) as chn:
        for key, value in boss_dict.items():
            chn.write(
                f'{key.strip()};{value};{translate_line_chn(value.strip())}\n'
            )


file_making()
