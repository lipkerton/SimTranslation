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

def parsing_binary_trans(
        path_dictionary: str
) -> dict:
    """Decoding orderer's dictionary."""

    line = ''
    new_dict = dict()
    with open(path_dictionary, 'rb') as sample:
        new = sample.read().decode('utf-16-le')
        line += new
    line = re.sub(
        lines_fixing_in_dictionary,
        '',
        line
    )
    line = line.split('耀')
    for i in range(2, len(line) - 1, 2):
        key = making_clean_string(key=line[i - 1])
        value = making_clean_string(value=line[i])
        new_dict[key] = (value, None)
    if (
        line[-2] not in new_dict.keys()
        and line[-1] not in new_dict.values()
    ):
        key = making_clean_string(key=line[-2])
        value = making_clean_string(value=line[-1])
        new_dict[key] = (value, None)
    return new_dict
