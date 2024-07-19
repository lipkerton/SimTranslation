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

    return new_dict


def get_updated_dictionary():

    updated_dict = dict()

    with open(
        path_for_temp_translations_eng, 'r', encoding='utf-8'
    ) as temp_eng:

        temp_eng_array = temp_eng.readlines()

        for index in range(len(temp_eng_array)):

            try:
                line = temp_eng_array[index].strip('\n').split(';')
                updated_dict[line[0].lower()] = line[1]

            except IndexError:
                raise IndexError(
                    'Something wrong in temp_english_dictionary '
                    f'file in line {index}. '
                    'Make sure you have used the correct format: '
                    'Russian word;English translation'
                )

    return updated_dict


def print_dictionary() -> None:
    """Creating decoded_dictionary.pkl."""

    sample_of_starting_dict = forming_dictionary(path_for_boss_dict)
    sample_updating_values = get_updated_dictionary()

    try:
        with open(path_for_main_dict, 'xb') as f:
            pickle.dump(sample_of_starting_dict, f)

    except FileExistsError:
        with open(path_for_main_dict, 'rb') as f:
            update_data = pickle.load(f)
            update_data.update(sample_updating_values)
        with open(path_for_main_dict, 'wb') as f:
            pickle.dump(update_data, f)
