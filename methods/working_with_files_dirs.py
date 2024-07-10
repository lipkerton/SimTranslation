from os import makedirs
import shutil

from .constants import path_for_translations_eng, path_for_translations_chn


def english_unpacking(temp_dictionary):

    global english_wordlist
    for key, value in english_wordlist.items():
        temp_dictionary.write(key.strip() + ';' + value + '\n')


def chinese_unpacking(temp_dictionary):

    global chinese_wordlist
    for key, value in chinese_wordlist.items():
        temp_dictionary.write(key.strip() + ';' + value + '\n')


def printing_eng_translations_into_csv(
        word: str, translated_word: str, file_name: str
) -> None:
    """Заносим переводы в csv в папку trans_csv_eng."""
    file_name.write(word.strip() + ';' + translated_word + '\n')


def printint_chn_translations_into_csv(
        word: str, translated_word: str, file_name: str
) -> None:
    pass


def chinese_recordings(
        word: str, translated_word: str
) -> None:
    global chinese_wordlist
    chinese_wordlist[word] = translated_word


def english_recordings(
        word: str, translated_word: str
) -> None:
    global english_wordlist
    english_wordlist[word] = translated_word


def chinese_one_file_exec(
        name_file: str
):
    file_chn_translations = open(
        f'{path_for_translations_chn}/{name_file}.csv',
        'a',
        encoding='utf-8'
    )
    return file_chn_translations


def english_one_file_exec(
        name_file: str
):
    file_eng_translations = open(
        f'{path_for_translations_eng}/{name_file}.csv',
        'a',
        encoding='utf-8'
    )
    return file_eng_translations


def making_rep(file_path):

    # macOS version
    new_file_path = '/'.join(
        file_path.split('/')[:-1]
    ).replace(
        'trans_input_files',
        'trans_result_files'
    )

    # windows version
    # new_file_path = '\\'.join(
    #     file_path.split('\\')[:-1]
    # ).replace(
    #     'trans_input_files',
    #     'trans_result_files'
    # )
    try:
        makedirs(new_file_path)
        return new_file_path
    except Exception:
        return new_file_path


def making_other_files(file):

    # macOS version
    name_file = file.split('/')[-1]
    new_dir = making_rep(file)
    shutil.copy2(file, f'{new_dir}/{name_file}')

    # windows version
    # name_file = file.split('\\')[-1]
    # new_dir = making_rep(file)
    # shutil.copy2(file, f'{new_dir}\\{name_file}')


chinese_wordlist = dict()
english_wordlist = dict()
