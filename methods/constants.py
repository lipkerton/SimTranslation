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

abs_paths_translated_fls = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/abs_paths_translated_fls.txt'
).absolute()
log_file = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/sim_log.log'
).absolute()
path_for_dict_csv = pathlib.Path(
    f'{project_dir}/dictionaries/base_translations.csv'
).absolute()
sql_dictionary_path = pathlib.Path(
    f'{project_dir}/dictionaries/translation.db'
)


#SQL Commands
create_table = '''
    CREATE TABLE translation (
    translation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rus VARCHAR(100) NOT NULL,
    eng VARCHAR(100),
    chn VARCHAR(100)
    );
'''
insert_values = 'INSERT OR REPLACE INTO translation (rus, eng, chn) VALUES(?, ?, ?);'
select_values = 'SELECT rus, eng, chn FROM translation'
