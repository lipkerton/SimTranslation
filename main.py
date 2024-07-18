from methods.constants import (path_dir_for_rus_files,
                               path_for_temp_translations_chn,
                               path_for_temp_translations_eng)
from methods.dictionary import print_dictionary
from methods.working_with_files_dirs import (chinese_unpacking,
                                             english_unpacking)
from methods.xml_line_parsing import parsing_xml


def main():

    print_dictionary()

    chinese_temp_dictionary = open(
        path_for_temp_translations_chn,
        'w',
        encoding='utf-8'
    )
    english_temp_dictionary = open(
        path_for_temp_translations_eng,
        'w',
        encoding='utf-8'
    )

    for file_path in path_dir_for_rus_files.rglob('*.*'):

        parsing_xml(str(file_path))

    chinese_unpacking(chinese_temp_dictionary)
    english_unpacking(english_temp_dictionary)

    chinese_temp_dictionary.close()
    english_temp_dictionary.close()

    print(
        'Files translation has been completed!\n'
        'Check trans_result_files to see a result.\n'
        'Check dictionaries/temp_[english/chinese]_dictionary.csv '
        'to see translations or to correct some mistakes.'
    )


if __name__ == '__main__':
    main()
