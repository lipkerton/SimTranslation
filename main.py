from methods.test_xml_line_parsing import parse_xml
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


input_path = pathlib.Path('../test_data/')
output_path = pathlib.Path('../test_results/')

if __name__ == '__main__':
    core_pattern(input_path=input_path, output_path=output_path, eng_or_chn='en')