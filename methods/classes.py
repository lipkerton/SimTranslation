import pathlib
import os
import shutil
import string
import argostranslate.package
import sqlite3
import logging

from .constants import abs_paths_translated_fls, path_for_dict_csv, log_file, sql_dictionary_path, create_table, insert_values, select_values


class RunSettings:
    def __init__(
            self,
            input_path: pathlib.Path,
            output_path: pathlib.Path,
            eng_or_chn: str
    ) -> None:
        self.log()
        self.abs_paths_open = open(abs_paths_translated_fls, 'w', encoding='utf-8')
        self.input_path = pathlib.Path(input_path)
        self.output_path = pathlib.Path(output_path)
        self.eng_or_chn = eng_or_chn
        self.acceptable_suffixes = ('.xprt', '.xml')
        self.num_lines = 0
        self.num_files = 0
        self.from_lang = "ru"
        self.argos_init()
        logging.info(f'Translating from "{self.from_lang}" to "{self.eng_or_chn}"...')

    def argos_init(self):

        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == self.from_lang
                and x.to_code == self.eng_or_chn,
                available_packages
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())

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
    
    def log(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename=log_file,
            mode='w',
            encoding='utf-8'
        )
        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(message)s'
            )
        )
        root_logger.addHandler(handler)


class DictionaryInit:

    def __init__(self) -> None:
        self.path_for_dict_csv = path_for_dict_csv
        self.temp_dict = dict()
        self.create_table()

    def get_specifics(self, words):
        try:
            if self.eng_or_chn == 'en':
                return words[0]
            if self.eng_or_chn == 'ch':
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
        """Parse temp_dict, get key and all values, insert it into DB."""
        for_insert_list = list()
        for key, value in data.items():
            sample = (key, value[0], value[1])
            for_insert_list.append(sample)
        self.insert_data(for_insert_list)

    def create_table(self):
        """Create a table if not exists."""
        with sqlite3.connect(sql_dictionary_path,  check_same_thread=False) as conn:
            curs = conn.cursor()
            try:
                curs.execute(create_table)
                data = self.take_csv_data()
                self.insert_data(data)
                conn.commit()
            except sqlite3.OperationalError as error:
                logging.error(error)

    def insert_data(self, data):
        """Insert data into DB."""
        with sqlite3.connect(sql_dictionary_path,  check_same_thread=False) as conn:
            curs = conn.cursor()
            curs.executemany(insert_values, data)
            conn.commit()

    def select_data(self) -> list:
        """Select data from DB."""
        with sqlite3.connect(sql_dictionary_path,  check_same_thread=False) as conn:
            curs = conn.cursor()
            curs.execute(select_values)
            rows = curs.fetchall()
        return rows
    
    # def delete_data(self):
    #     # что блять?
    #     self.open_connection()
    #     self.curs.execute(select_values)
    #     self.close_connection()

    def is_in_db(self, word):
        with sqlite3.connect(sql_dictionary_path,  check_same_thread=False) as conn:
            curs = conn.cursor()
            temp_dict_words = self.temp_dict.get(word, None)
            curs.execute(f"{select_values} WHERE rus = '{word}';")
            rows = curs.fetchone()
        if rows:
            return (rows[1], rows[2])
        if temp_dict_words:
            return temp_dict_words


class Word:

    def __init__(self, word) -> None:
        self.word = word
        self.clean_word = word.strip(
            string.whitespace
        )