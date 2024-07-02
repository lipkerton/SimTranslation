from methods.xml_line_parsing import parsing_xml
from methods.dictionary import print_dictionary
from methods.constants import path_dir_for_rus_files


def main():
    print_dictionary()
    for file_path in path_dir_for_rus_files.rglob('*.*'):
        parsing_xml(str(file_path))

if __name__ == '__main__':
    main()
