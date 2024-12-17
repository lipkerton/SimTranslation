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
# path_for_main_dict = pathlib.Path(
#     f'{project_dir}/dictionaries/decoded_dictionary.pkl'
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
    f'{project_dir}/dictionaries/base_translations.csv'
).absolute()
dictionary_current_state_txt = pathlib.Path(
    f'{project_dir}/dictionaries/dictionary_current_state.txt'
).absolute()
dictionary_current_state_csv = pathlib.Path(
    f'{project_dir}/dictionaries/dictionary_current_state.csv'
).absolute()
sql_dictionary_path = pathlib.Path(
    f'{project_dir}/dictionaries/translations.db'
)