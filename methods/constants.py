import os
import pathlib

# manual launch version (through main.py)
project_dir = str(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# exe version
# project_dir = str(
#     os.path.dirname(
#         os.path.dirname(
#             os.path.dirname(
#                 os.path.dirname(
#                     os.path.abspath(__file__)
#                 )
#             )
#         )
#     )
# )
path_dir_for_rus_files = pathlib.Path(
    f'{project_dir}/trans_input_files'
).absolute()
path_for_translations_eng = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/trans_csv_eng'
).absolute()
path_for_translations_chn = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/trans_csv_eng'
).absolute()
path_for_temp_translations_chn = pathlib.Path(
    f'{project_dir}/dictionaries/temp_chinese_dictionary.csv'
).absolute()
path_for_temp_translations_eng = pathlib.Path(
    f'{project_dir}/dictionaries/temp_english_dictionary.csv'
)
path_for_boss_dict = pathlib.Path(
    f'{project_dir}/dictionaries/maintranslation.trans'
).absolute()
path_for_main_dict = pathlib.Path(
    f'{project_dir}/dictionaries/decoded_dictionary.pkl'
).absolute()

lines_fixing_in_dictionary = (
    r'[\x19\x0c\x10\x17\x07\x13\x16\x1f\x14\x07\x0f\x8a\xb2'
    r'\x1d\x1c\x1e\x1a\x12\x1b\n\x0b\x08\x0e\r\t\x01'
    r'\x18\x11\x15\x05\x04\x03\x06\x90\x02\x81\xb3'
    r'\u2080\u2081\u2082\ufeff\u03b4\u200b\u03c4\u2265'
    r'\u03c9\u2260\u2264\u22bb\u03b2]'
)
