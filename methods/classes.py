import pathlib
import os
import pickle
import shutil
import string
from .constants import abs_paths_translated_fls, path_for_translations_chn, path_for_translations_eng, path_for_main_dict, path_for_dict_csv, logs, dictionary_current_state_txt, dictionary_current_state_csv


class RunSettings:
    def __init__(
            self,
            input_path: pathlib.Path,
            output_path: pathlib.Path,
            eng_or_chn: str
    ) -> None:
        self.abs_paths_open = open(abs_paths_translated_fls, 'w', encoding='utf-8')
        self.input_path = pathlib.Path(input_path)
        self.output_path = pathlib.Path(output_path)
        self.eng_or_chn = eng_or_chn
        self.csv_file = None
        self.input_file = None
        self.file_name = None
        self.file_suffix = None
        self.acceptable_suffixes = ('.xprt', '.xml')
        if eng_or_chn == 'English':
            self.eng_or_chn = 'en'
        else:
            self.eng_or_chn = 'zh-cn'
        self.num_lines = 0
        self.num_files = 0

    def input_file_push(self, file):
        self.input_file = pathlib.Path(file)
        self.file_name = pathlib.Path(self.input_file).name.split('.')[0]
        self.file_suffix = pathlib.Path(self.input_file).suffix

    def output_folder_path(self):
        self.output_folder = pathlib.Path(
            str(self.input_file).replace(
                str(self.input_path),
                str(self.output_path)
            )
        ).parent
        self.output_folder_create()
        return self.output_folder
    
    def output_folder_create(self):
        try:
            os.makedirs(self.output_folder)
        except OSError:
            pass
    
    def create_copies_of_files(self):
        output_folder = self.output_folder_path()
        shutil.copy2(self.input_file, f'{output_folder}/{self.file_name}')
    
    def is_suffix(self):
        if self.file_suffix in self.acceptable_suffixes:
            return True
        self.create_copies_of_files()
        return False
    
    def csv_path(self):
        if self.eng_or_chn == 'en':
            return path_for_translations_eng
        elif self.eng_or_chn == 'zh-cn':
            return path_for_translations_chn

    def csv_done_translations(self, all_values):
        csv_translations_path = self.csv_path()
        with open(csv_translations_path, 'a', encoding='utf-8') as csv:
            for key, value in sorted(all_values, key=lambda x: x[0], reverse=True):
                core_message = f'{key};{value[0]};{value[1]}\n'
                csv.write(core_message)
    
    def compile_result_message(self):
        """Compile summary message for output window."""
        return (
            f'{self.file_name} was translated!\n'
            f'File number: {self.num_files}\n'
            f'Translated lines counter: {self.num_lines}\n'
            '\n'
        )
    
    def abs_paths_txt_update(self, new_path):
        new_path = pathlib.Path(new_path)
        new_path = str(new_path) + '\n'
        self.abs_paths_open.write(new_path)
    
    def abs_paths_txt_close(self):
        self.abs_paths_open.close()
    
    def print_in_logs(self, message):
        with open(logs, 'w', encoding='utf-8') as log:
            log.write(message)


class DictionaryInit:

    def __init__(self) -> None:
        self.path_for_main_dict = path_for_main_dict
        self.path_for_dict_csv = path_for_dict_csv
        self.dictionary_current_state_txt = dictionary_current_state_txt
        self.dictionary_current_state_csv = dictionary_current_state_csv
        self.temp_dict = dict()
        if not self.pkl_is_formed():
            self.pkl_create()
        with open(self.path_for_main_dict, 'rb') as cd:
            self.core_dict = pickle.load(cd)
        self.txt_create_update()
        self.csv_create_update()

    def is_in_dictionary(self, word):
        core_dict_words = self.core_dict.get(word, None)
        temp_dict_words = self.temp_dict.get(word, None)
        if core_dict_words:
            return core_dict_words
        elif temp_dict_words:
            return temp_dict_words
    
    def pkl_is_formed(self):
        return os.path.exists(self.path_for_main_dict)
    
    def get_specifics(self, words):
        try:
            if self.eng_or_chn == 'en':
                return words[0]
            if self.eng_or_chn == 'zh-cn':
                return words[1]
        except IndexError:
            return None
        except TypeError:
            return None

    def eng_or_chn_set(self, setting):
        self.eng_or_chn = setting
    
    def take_csv_data(self):
        return_dict=dict()
        with open(
            self.path_for_dict_csv, 'r', encoding='utf-8'
        ) as csv:
            for line in csv.readlines():
                line = line.strip('\n').split(';')
                key, value, additional_value = (
                    line[0].lower(), line[1], line[2]
                )
                return_dict[key] = (value, additional_value)
        return return_dict

    def take_update_data(self, changes):
        """Parse changes, form update and send it to pkl_uodate."""
        update = dict()
        for line in changes:
            if line:
                line = line.strip().split(';')
                russian_word = line[0].strip().lower()
                english_word = line[1].strip()
                chinese_word = line[2].strip()
                update[russian_word] = (english_word, chinese_word)
        if update:
            self.pkl_update(update)

    def pkl_create(self) -> None:
        """Creating decoded_dictionary.pkl."""
        with open(self.path_for_main_dict, 'xb') as pkl:
            csv_data = self.take_csv_data()
            pickle.dump(csv_data, pkl)
        
    def pkl_update(self, update):
        with open(self.path_for_main_dict, 'rb') as pkl:
            pkl_data = pickle.load(pkl)
            pkl_data.update(update)
        with open(self.path_for_main_dict, 'wb') as pkl:
            pickle.dump(pkl_data, pkl)
        with open(self.path_for_main_dict, 'rb') as pkl:
            self.core_dict = pickle.load(pkl)
        self.temp_dict = dict()
    
    def txt_create_update(self) -> None:
        with open(self.path_for_main_dict, 'rb') as pkl:
            pkl_data = pickle.load(pkl)
        with open(self.dictionary_current_state_txt, 'w', encoding='utf-8') as txt:
            for key, value in pkl_data.items():
                message = f'{key}   ;   {value[0]}   ;   {value[1]}\n'
                txt.write(message)

    def csv_create_update(self):
        with open(self.path_for_main_dict, 'rb') as pkl:
            pkl_data = pickle.load(pkl)
        with open(self.dictionary_current_state_csv, 'w', encoding='utf-8') as csv:
            for key, value in pkl_data.items():
                message = f'{key};{value[0]};{value[1]}\n'
                csv.write(message)


class Word:

    def __init__(self, word) -> None:
        self.word = word
        self.clean_word = word.strip(
            string.whitespace
        ).lower()