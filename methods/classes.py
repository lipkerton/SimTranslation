import pathlib
import os
import shutil
import string
from .constants import abs_paths_translated_fls, path_for_translations_chn, path_for_translations_eng, path_for_dict_csv, logs, dictionary_current_state_txt, dictionary_current_state_csv, sql_dictionary_path
import sqlite3
from .constants import create_table, insert_values, select_values


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
        self.eng_or_chn = eng_or_chn
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
        self.path_for_dict_csv = path_for_dict_csv
        self.dictionary_current_state_txt = dictionary_current_state_txt
        self.dictionary_current_state_csv = dictionary_current_state_csv
        self.temp_dict = dict()
        self.create_table()
        self.txt_create_update()
        self.csv_create_update()

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
    
    def take_csv_data(self) -> tuple:
        return_list=list()
        with open(
            self.path_for_dict_csv, 'r', encoding='utf-8'
        ) as csv:
            for line in csv.readlines():
                line = line.strip('\n').split(';')
                key, value, additional_value = (
                    line[0], line[1], line[2]
                )
                data = (key, value, additional_value)
                return_list.append(data)
        return return_list

    def take_update_data(self, changes, truncate=False):
        """Parse changes, form update and send it to pkl_uodate."""
        for_insert_list = list()
        for line in changes:
            if line:
                line = line.strip().split(';')
                russian_word = line[0].strip()
                english_word = line[1].strip()
                chinese_word = line[2].strip()
                data = (russian_word, english_word, chinese_word)
                for_insert_list.append(data)
        if truncate:
            self.delete_data()
        self.insert_data(for_insert_list)

    def take_temp_data(self, data):
        for_insert_list = list()
        for key, value in data.items():
            sample = (key, value[0], value[1])
            for_insert_list.append(sample)
        self.insert_data(for_insert_list)

    def create_table(self):
        self.open_connection()
        try:
            self.curs.execute(create_table)
            data = self.take_csv_data()
            self.insert_data(data)

        except sqlite3.OperationalError:
            self.conn.commit()
            self.close_connection()


    def insert_data(self, data):
        self.open_connection()
        self.curs.executemany(insert_values, data)
        self.conn.commit()
        self.close_connection()


    def select_data(self) -> list:
        self.open_connection()
        self.curs.execute(select_values)
        rows = self.curs.fetchall()
        self.close_connection()
        return rows
    
    def delete_data(self):
        # что блять?
        self.open_connection()
        self.curs.execute(select_values)
        self.close_connection()

    def is_in_db(self, word):
        self.open_connection()
        temp_dict_words = self.temp_dict.get(word, None)
        self.curs.execute(f"{select_values} WHERE rus = '{word}';")
        rows = self.curs.fetchone()
        self.close_connection()
        if rows:
            return (rows[1], rows[2])
        if temp_dict_words:
            return temp_dict_words

    def txt_create_update(self) -> None:
        data = self.select_data()
        with open(self.dictionary_current_state_txt, 'w', encoding='utf-8') as txt:
            for rus, eng, chn in data:
                message = f'{rus}   ;   {eng}   ;   {chn}\n'
                txt.write(message)

    def csv_create_update(self):
        data = self.select_data()
        with open(self.dictionary_current_state_csv, 'w', encoding='utf-8') as csv:
            for rus, eng, chn in data:
                message = f'{rus};{eng};{chn}\n'
                csv.write(message)

    def open_connection(self):
        self.conn = sqlite3.connect(sql_dictionary_path,  check_same_thread=False)
        self.curs = self.conn.cursor()

    def close_connection(self):
        self.curs.close()
        self.conn.close()


class Word:

    def __init__(self, word) -> None:
        self.word = word
        self.clean_word = word.strip(
            string.whitespace
        )