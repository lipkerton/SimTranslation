import os
import pathlib
from googletrans import Translator

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

path_for_translations_eng = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/trans_csv_eng'
).absolute()
path_for_translations_chn = pathlib.Path(
    f'{project_dir}/trans_support_files_dirs/trans_csv_chn'
).absolute()
path_for_boss_dict_eng = pathlib.Path(
    f'{project_dir}/dictionaries/maintranslation.trans'
).absolute()
path_for_boss_dict = pathlib.Path(
    f'{project_dir}/dictionaries/chn_base_dictionary.csv'
).absolute()
path_for_main_dict = pathlib.Path(
    f'{project_dir}/dictionaries/decoded_dictionary.pkl'
).absolute()
media_directory = pathlib.Path(
    f'{project_dir}/media'
).absolute()
output_folder = pathlib.Path(
    f'{project_dir}/output'
).absolute()

exceptions_extez = ('.xprt', '.xml')
exceptions_dots = ("'", "`", '"')

save_changes = 'Save changes'
undo_changes = 'Undo changes'

iter_tags = ('plot', 'bottomaxis', 'leftaxis', 'series')
child_names = ('labeltext', 'text', 'caption')

translator = Translator()

# lines_fixing_in_dictionary = (
#     r'[\x19\x0c\x10\x17\x07\x13\x16\x1f\x14\x07\x0f\x8a\xb2'
#     r'\x1d\x1c\x1e\x1a\x12\x1b\n\x0b\x08\x0e\r\t\x01'
#     r'\x18\x11\x15\x05\x04\x03\x06\x90\x02\x81\xb3'
#     r'\u2080\u2081\u2082\ufeff\u03b4\u200b\u03c4\u2265'
#     r'\u03c9\u2260\u2264\u22bb\u03b2]'
# )
