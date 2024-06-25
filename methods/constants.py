import os
import pathlib

project_dir = str(os.path.dirname(os.path.abspath(__file__)))
path_dir_for_rus_files = pathlib.Path('./trans_input_files').resolve()
path_for_translations_eng = pathlib.Path('./trans_csv_eng').resolve()
path_for_translations_chn = pathlib.Path('./trans_csv_chn').resolve()
path_for_boss_dict = pathlib.Path('./dictionaries/maintranslation.trans')
path_for_main_dict = pathlib.Path('./dictionaries/decoded_dictionary.pkl')

lines_fixing_in_dictionary = (
    r'[\x19\x0c\x10\x17\x07\x13\x16\x1f\x14\x07\x0f'
    r'\x1d\x1c\x1e\x1a\x12\x1b\n\x0b\x08\x0e\r\t'
    r'\x18\x11\x15\x05\x04\x03\x06\x90\u200b]'
)
