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


#SQL Commands
create_table = '''
    CREATE TABLE translation(
    translation_id BIGINT GENERATED ALWAYS AS IDENTITY RPIMARY KEY,
    rus VARCHAR(100) NOT NULL,
    eng VARCHAR(100),
    chn VARCHAR(100)
    );
'''
insert_values = 'INSERT OR REPLACE INTO translation (rus, eng, chn) VALUES(?, ?, ?);'
select_values = 'SELECT rus, eng, chn FROM translation'
