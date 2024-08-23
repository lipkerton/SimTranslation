import shutil
from os import makedirs
from pathlib import Path

from .constants import exceptions_extez


def printing_translations_into_csv(
        word: str,
        translated_word: str,
        file_name: str
) -> None:
    """We put translations in csv in the trans_csv_eng folder."""
    file_name.write(word.strip() + ';' + translated_word + '\n')


def one_file_exec(
        name_file: str,
        path_for_translations: Path
):
    """We create a separate csv file to record
    translations for each project."""
    file_translations = open(
        f'{path_for_translations}/{name_file}.csv',
        'a',
        encoding='utf-8'
    )
    return file_translations


def check_file_extenz(
    CORE_SETTINGS
) -> bool:
    """Checking file extension."""
    extenz = Path(CORE_SETTINGS.input_file).suffix
    if extenz not in exceptions_extez:
        making_other_files(
            CORE_SETTINGS
        )
        return False
    return True


def making_rep(
    CORE_SETTINGS
) -> Path:
    """Making directories for future files."""
    input_file = str(CORE_SETTINGS.input_file)
    new_file_path = Path(
        input_file.replace(
            str(CORE_SETTINGS.input_folder),
            str(CORE_SETTINGS.output_folder)
        )
    ).parent
    try:
        makedirs(new_file_path)
    except Exception:
        pass
    return new_file_path


def making_other_files(
    CORE_SETTINGS
) -> None:
    """Making copies of files which we're not going to translate
    and place them on the same places which they have in original rep."""
    name_file = Path(CORE_SETTINGS.input_file).name
    new_dir = making_rep(CORE_SETTINGS)
    shutil.copy2(CORE_SETTINGS.input_file, f'{new_dir}/{name_file}')
