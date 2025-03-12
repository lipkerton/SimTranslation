from methods.test_interface import base_window_init
from methods.test_xml_line_parsing import parse_xml, dictionaries
from methods.classes import RunSettings
import pathlib


def core_pattern(
    input_path,
    output_path,
    eng_or_chn
) -> None:
    settings = RunSettings(
        input_path=input_path,
        output_path=output_path,
        eng_or_chn=eng_or_chn
    )
    try:
        for file_path in settings.input_path.rglob('*.*'):
            settings.input_file_push(file_path)
            if settings.is_suffix():
                message = parse_xml(settings)
                print(message)
    except PermissionError as error:
        message = f'{error}'
        settings.print_in_logs(message=message)
    settings.abs_paths_txt_close()
    settings.csv_done_translations(
        dictionaries.temp_dict.items()
    )


input_path = pathlib.Path('F:\gsdfs\work\Тестовые примеры SimInTech\input')
output_path = pathlib.Path('F:\gsdfs\work\Тестовые примеры SimInTech\output')

if __name__ == '__main__':
    core_pattern(input_path=input_path, output_path=output_path, eng_or_chn='en')