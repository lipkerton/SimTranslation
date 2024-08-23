import pickle
import platform
import string
import os
from pathlib import Path

from .working_with_files_dirs import one_file_exec
from.translation_chn_eng import translated_line_construction, check_the_word_in_dict
from .dictionary import print_into_dictionary, quick_update
from .constants import (
    path_for_main_dict,
    path_for_translations_eng,
    path_for_translations_chn,
    output_folder,
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
        """Create decoded_dictionary.pkl"""
        print_into_dictionary()

    def dictionaries_update(self, update):
        """Save changes in decoded_dictionary.pkl"""
        quick_update(update)

    def saved_dict_close(self):
        """Closing pickle dictionaries."""
        self.base_temp_dict = dict()
        self.saved_dict.close()
    
    def compile_message(self):
        """Compile summary message for output window."""
        message = (
            f'{self.name_file} was translated!\n'
            f'File number: {self.num_files}\n'
            f'Translated lines counter: {self.num_lines}\n'
            '\n'
        )
        return message

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


class WordTranslate:

    def __init__(self, word, CORE_SETTINGS) -> None:
        self.init_word = word
        self.clean_word = word.strip(
            string.punctuation + string.punctuation
        )
        self.CORE_SETTINGS = CORE_SETTINGS
    
    def prep_translated_word(self):
        self.translated_word = check_the_word_in_dict(self)


class LineTranslate:
    """The line is coming from parsing_xml func
    searching for rus words in line and send them to
    translation_chn_eng.py"""

    def __init__(self, line, CORE_SETTINGS) -> None:
        self.line = line
        self.translated_line = line
        self.wordlist = list()
        self.exceptions_dots = ("'", "`", '"')
        self.alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        self.translator_flag = self.match(line)
        self.CORE_SETTINGS = CORE_SETTINGS

    def match(
            self, text: str
    ) -> bool:
        """Checking line for russian letters."""
        if text is not None:
            return not self.alphabet.isdisjoint(text.lower())

    def core_parse_line(
            self
    ) -> None:
        """Parsing line that we need to translate,
        searching for any words in quotes,
        send them into sorted wordlist.
        Sorted list is going to be send in
        words_in_line_translate func below."""
        RUS_TEXT = str()
        FLAG = False
        for symbol_index in range(len(self.line) - 1):
            if FLAG:
                RUS_TEXT += self.line[symbol_index]
            if self.line[symbol_index] in self.exceptions_dots:
                FLAG = True
            if self.line[symbol_index + 1] in self.exceptions_dots:
                self.wordlist.append(RUS_TEXT)
                RUS_TEXT = str()
                FLAG = False
        self.wordlist = sorted(self.wordlist, key=len, reverse=True)

    def words_in_line_translate(
            self, file_name=None
    ) -> str:
        """Iterating through wordlist
        check-in every word for russion letters
        sending each word into word_separation_in_two func."""
        for word in self.wordlist:
            if self.match(word):
                word_obj = WordTranslate(word, self.CORE_SETTINGS)
                translated_line_construction(self, word_obj)
        if file_name:
            if self.match(file_name):
                word_obj = WordTranslate(file_name, self.CORE_SETTINGS)
                translated_line_construction(self, word_obj)
        return self.translated_line
