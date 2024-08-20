import pickle
import platform
import os
from pathlib import Path

from .working_with_files_dirs import one_file_exec
from .dictionary import print_into_dictionary, quick_update
from .constants import (
    path_for_main_dict,
    path_for_translations_eng,
    path_for_translations_chn,
    output_folder
)


class PrepParseObj:
    """Input file (path to it) which we need to translate
    with support characteristics such as path to input/output folders
    language, name of the file and samples of dictionaries."""
    def __init__(
            self,
    ) -> None:
        self.output_folder = output_folder
        self.base_temp_dict = dict()
        self.wordlist = dict()
        self.num_files = 0
        self.num_lines = 0
        if platform.system().lower() == 'windows':
            self.plat = 'win'
        elif platform.system().lower() == 'darwin':
            self.plat = 'mac'
        else:
            self.plat = 'mac'

    def input_path_push(self, input_path):
        """Path to folder from GUI."""
        self.input_folder = Path(input_path)

    def output_path_push(self, output_path):
        """Path to folder from GUI."""
        self.output_folder = Path(output_path)

    def create_output_folder(self):
        """output dir creation."""
        try:
            os.mkdir(self.output_folder)
        except Exception:
            pass
        return self.output_folder

    def language_push(self, language: str):
        """Language from GUI."""
        self.language = language
        if language == 'English':
            self.abs_for_translator = 'en'
        else:
            self.abs_for_translator = 'zh-cn'

    def file_path_push(self, path):
        """File need to be translated from core_pattern in main.py."""
        self.input_file = path
        self.name_file = Path(path).name.split('.')[0]

    def one_file_exec(self):
        """Open .csv file to print words have been
        translated project per project."""
        if self.language == 'English':
            self.files_translations = (
                one_file_exec(
                    self.name_file,
                    path_for_translations_eng
                )
            )
        else:
            self.files_translations = (
                one_file_exec(
                    self.name_file,
                    path_for_translations_chn
                )
            )

    def temp_dict_push(self, key, value=None, additional_value=None):
        """This dict is needed to print translations
        per each file in one translation session. In previous versions
        large projects overloaded the main translation pattern cause
        there were many similar words and each of them were
        translated as new one."""
        self.base_temp_dict[key] = (value, additional_value)

    def dictionaries_init(self):
        """Inititalization of pickle_dictionaries."""
        self.saved_dict = open(path_for_main_dict, 'rb')
        self.boss_dict = pickle.load(self.saved_dict)

    def dictionaries_creation(self):
        print_into_dictionary()

    def dictionaries_update(self, update):
        quick_update(update)

    def saved_dict_close(self):
        """Closing pickle dictionaries."""
        self.base_temp_dict = dict()
        self.saved_dict.close()

    def upd_files_counter(self, zeroed=False):
        """It is for messages that translation session was complete."""
        if not zeroed:
            self.num_files += 1
        else:
            self.num_files = 0

    def upd_lines_counter(self, zeroed=False):
        """It is for messages that translation session was complete."""
        if not zeroed:
            self.num_lines += 1
        else:
            self.num_lines = 0
