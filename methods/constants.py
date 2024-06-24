import os
import pathlib

project_dir = str(os.path.dirname(os.path.abspath(__file__)))
path_dir_for_rus_files = pathlib.Path('./trans_input_files').resolve()
path_for_translations_eng = pathlib.Path('./trans_csv_eng').resolve()
path_for_translations_chn = pathlib.Path('./trans_csv_chn').resolve()
path_for_boss_dict = pathlib.Path('./dictionaries/maintranslation.trans')
path_for_main_dict = pathlib.Path('./dictionaries/decoded_dictionary.pkl')
