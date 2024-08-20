import pickle

from .constants import (
    path_for_boss_dict,
    path_for_main_dict
)


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
                '/&$-,=+@[;:<#$%*"!?\'\n '
            )
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
            key = making_clean_string(key=line[0])
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


def quick_update(changes):
    updated_dict = dict()
    for index in range(len(changes)):
        if changes[index]:
            try:
                line = changes[index].strip('\n').split(';')
                word_to = making_clean_string(key=line[0])
                translate = making_clean_string(value=line[1])
                if len(line) == 2:
                    updated_dict[word_to] = (translate, None)
                elif len(line) == 3:
                    additional_value = making_clean_string(value=line[2])
                    updated_dict[word_to] = (translate, additional_value)
                else:
                    raise IndexError('Wrong format!')
            except IndexError:
                subindex = len(changes[index])
                return (index, subindex)
    print_into_dictionary(
        updated_dict
    )
