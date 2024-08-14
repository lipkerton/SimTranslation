import pickle
import re

from .constants import (lines_fixing_in_dictionary, path_for_boss_dict_chn,
                        path_for_boss_dict_eng, path_for_main_dict_chn,
                        path_for_main_dict_eng)


def making_clean_string(
        key=None, value=None
) -> str:
    """Kicking off some trash from the line."""

    if key is not None:
        result = key.strip(
                '/&$-,=+@[;:<#$%*"!?\' '
            ).lower()

    elif value is not None:
        result = value.strip(
                '/&$-,=+@[;:<#$%*"!?\' '
            )
    return result


def forming_dictionary_eng(
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


def forming_dictionary_chn(
        path_dictionary: str
) -> dict:

    new_dict = dict()

    with open(
        path_dictionary, 'rb', encoding='utf-8'
    ) as sample:

        for line in sample.readlines():
            line = line.split(';')
            key = making_clean_string(key=line[1])
            value = making_clean_string(value=line[2])
            new_dict[key] = value

    return new_dict


def quick_update(changes, language):

    updated_dict = dict()

    for index in range(len(changes)):
        if changes[index] != '':
            try:
                line = changes[index].split(';')
                word_to = making_clean_string(key=line[0])
                translate = making_clean_string(value=line[1])
                updated_dict[word_to] = translate

            except IndexError:
                subindex = len(changes[index])
                return (index, subindex)
    if language == 'English':
        print_into_dictionary_eng(updated_dict)
    else:
        print_into_dictionary_chn(updated_dict)


def print_into_dictionary_eng(update=None) -> None:
    """Creating decoded_dictionary.pkl."""

    try:
        with open(path_for_main_dict_eng, 'xb') as f:
            sample_of_starting_dict = forming_dictionary_eng(
                path_for_boss_dict_eng
            )
            if update is not None:
                sample_of_starting_dict.update(update)
            pickle.dump(sample_of_starting_dict, f)

    except FileExistsError:
        with open(path_for_main_dict_eng, 'rb') as f:
            update_data = pickle.load(f)
            if update is not None:
                update_data.update(update)
        with open(path_for_main_dict_eng, 'wb') as f:
            pickle.dump(update_data, f)


def print_into_dictionary_chn(update=None) -> None:
    """Creating decoded_dictionary.pkl."""

    try:
        with open(path_for_main_dict_chn, 'xb') as f:
            sample_of_starting_dict = forming_dictionary_chn(
                path_for_boss_dict_chn
            )
            if update is not None:
                sample_of_starting_dict.update(update)
            pickle.dump(sample_of_starting_dict, f)

    except FileExistsError:
        with open(path_for_main_dict_chn, 'rb') as f:
            update_data = pickle.load(f)
            if update is not None:
                update_data.update(update)
        with open(path_for_main_dict_chn, 'wb') as f:
            pickle.dump(update_data, f)
