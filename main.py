from methods.test_xml_line_parsing import parse_xml
from methods.classes import RunSettings
import pathlib
import logging


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
                logging.info(f'Translating {file_path}...')
                parse_xml(settings)
                logging.info(f'Translation of {file_path} fineshed!')
    except PermissionError as error:
        logging.error(error)
    settings.abs_paths_txt_close()


input_path = pathlib.Path('F:\gsdfs\work\Тестовые примеры SimInTech\input')
output_path = pathlib.Path('F:\gsdfs\work\Тестовые примеры SimInTech\output')

if __name__ == '__main__':
    core_pattern(input_path=input_path, output_path=output_path, eng_or_chn='en')