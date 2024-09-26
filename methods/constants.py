import os
import pathlib

# manual launch version (through main.py)
# project_dir = str(
#     os.path.dirname(
#         os.path.dirname(
#             os.path.abspath(__file__)
#         )
#     )
# )


# exe version
project_dir = str(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
    )
)
# path_for_boss_dict_eng = pathlib.Path(
#     f'{project_dir}/dictionaries/maintranslation.trans'
# ).absolute()
# media_directory = pathlib.Path(
#     f'{project_dir}/media'
# ).absolute()
# output_folder = pathlib.Path(
#     f'{project_dir}/output'
# ).absolute()

path_for_translations_eng = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/trans_csv_eng/all_translations.csv'
).absolute()
path_for_translations_chn = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/trans_csv_chn/all_translations.csv'
).absolute()
abs_paths_translated_fls = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/abs_paths_translated_fls.txt'
).absolute()
logs = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/logs.txt'
).absolute()
path_for_dict_csv = pathlib.Path(
    f'{project_dir}/dictionaries/chn_base_dictionary.csv'
).absolute()
path_for_main_dict = pathlib.Path(
    f'{project_dir}/dictionaries/decoded_dictionary.pkl'
).absolute()
dictionary_current_state_txt = pathlib.Path(
    f'{project_dir}/dictionaries/dictionary_current_state.txt'
).absolute()
dictionary_current_state_csv = pathlib.Path(
    f'{project_dir}/dictionaries/dictionary_current_state.csv'
).absolute()


# lines_fixing_in_dictionary = (
#     r'[\x19\x0c\x10\x17\x07\x13\x16\x1f\x14\x07\x0f\x8a\xb2'
#     r'\x1d\x1c\x1e\x1a\x12\x1b\n\x0b\x08\x0e\r\t\x01'
#     r'\x18\x11\x15\x05\x04\x03\x06\x90\x02\x81\xb3'
#     r'\u2080\u2081\u2082\ufeff\u03b4\u200b\u03c4\u2265'
#     r'\u03c9\u2260\u2264\u22bb\u03b2]'
# )
