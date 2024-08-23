import pickle
import string

from .constants import (
    path_for_boss_dict,
    path_for_main_dict
)


def making_clean_string(
        value, low=False
) -> str:
    """Kicking off some trash from the line."""
    result = value.strip(
        string.punctuation + string.whitespace
    )
    if low:
        result = result.lower()
    return result


def forming_dictionary(
        path_dictionary: str
) -> dict:
    new_dict = dict()
    with open(
        path_dictionary, 'r', encoding='utf-8'
    ) as sample:
        for line in sample.readlines():
            line = line.strip('\n').split(';')
            key = making_clean_string(value=line[0], low=True)
            value = making_clean_string(value=line[1])
            additional_value = making_clean_string(value=line[2])
            new_dict[key] = (value, additional_value)
    return new_dict


def print_into_dictionary(update=None) -> None:
    """Creating decoded_dictionary.pkl."""
    try:
        with open(path_for_main_dict, 'xb') as f:
            sample_of_starting_dict = forming_dictionary(
                path_for_boss_dict
            )
            if update is not None:
                sample_of_starting_dict.update(update)
            pickle.dump(sample_of_starting_dict, f)
    except FileExistsError:
        with open(path_for_main_dict, 'rb') as f:
            update_data = pickle.load(f)
            if update is not None:
                update_data.update(update)
        with open(path_for_main_dict, 'wb') as f:
            pickle.dump(update_data, f)


def quick_update(
        changes
) -> None:
    """Changes is a line that looks like this:
    <rus_word;eng_word;chn_word>
    we split this line in three parts and send them
    in print_into_dictionary func
    if something went wrong there will be IndexError
    wrong formed words will be displayed in GUI."""
    updated_dict = dict()
    for index in range(len(changes)):
        if changes[index]:
            line = changes[index].strip('\n').split(';')
            word_to = making_clean_string(value=line[0], low=True)
            translate = making_clean_string(value=line[1])
            if len(line) == 2:
                updated_dict[word_to] = (translate, None)
            elif len(line) == 3:
                additional_value = making_clean_string(value=line[2])
                updated_dict[word_to] = (translate, additional_value)
    print_into_dictionary(
        updated_dict
    )
