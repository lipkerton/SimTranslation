import pickle
import re

from .constants import (lines_fixing_in_dictionary, path_for_boss_dict,
                        path_for_main_dict,
                        path_for_temp_translations_eng)


def making_clean_string(
        key=None, value=None
) -> str:
    """Kicking off some trash from the line."""

    if key is not None:
        result = key.strip(
                '/&$-,.=+@[;:<#$%*"!?\' '
            ).lower()

    elif value is not None:
        result = value.strip(
                '/&$-,.=+@[;:<#$%*"!?\' '
            )
    return result


def forming_dictionary(
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

        new_dict[key] = value

    if (
        line[-2] not in new_dict.keys()
        and line[-1] not in new_dict.values()
    ):

        key = making_clean_string(key=line[-2])
        value = making_clean_string(value=line[-1])

        new_dict[key] = value

    with open(
        path_for_temp_translations_eng, 'r', encoding='utf-8'
    ) as temp_eng:

        for line in temp_eng.readlines():
            line = line.strip('\n').split(';')
            new_dict[line[0]] = line[1]

    return new_dict


def print_dictionary() -> None:
    """Creating decoded_dictionary.pkl."""
    sample_of_starting_dict = forming_dictionary(path_for_boss_dict)
    with open(path_for_main_dict, 'wb') as f:
        pickle.dump(sample_of_starting_dict, f)
