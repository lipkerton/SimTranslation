import pickle
import re

from .constants import (
    path_for_boss_dict, path_for_main_dict, lines_fixing_in_dictionary
)


def forming_dictionary(path_dictionary):
    """Раскодируем словарь заказчика"""
    file_name = path_dictionary

    line = ''
    new_dict = dict()

    with open(file_name, 'rb') as sample:
        new = sample.read().decode('utf-16-le')
        line += new

    line = re.sub(
        lines_fixing_in_dictionary,
        '',
        line
    )
    line = line.split('耀')

    for i in range(2, len(line) - 1, 2):

        key = line[i - 1].strip(
            '/&$-,.=+@[;:<#$%*"!\''
        )
        value = line[i].strip(
            '/&$-,.=+@[;:<#$%*"!\''
        )
        new_dict[key.strip().lower()] = value.strip()

    if line[-2] not in new_dict.keys():

        key = line[-2].strip(
            '/&$-,.=+@[;:<#$%*"!\'('
        )
        value = line[-1].strip(
            '/&$-,.=+@[;:<#$%*"!\'('
        )
        new_dict[key] = value

    return new_dict


def print_dictionary():
    sample_of_starting_dict = forming_dictionary(path_for_boss_dict)
    with open(path_for_main_dict, 'wb') as f:
        pickle.dump(sample_of_starting_dict, f)
