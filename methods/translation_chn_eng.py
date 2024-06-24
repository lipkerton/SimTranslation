from googletrans import Translator

from .working_with_files_dirs import (chinese_recordings,
                                      printing_translations_into_txt)


def match(
        text: str, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
):
    """Проверка строки на русские символы."""

    if text is not None:
        return not alphabet.isdisjoint(text.lower())
    else:
        return text


def translate_file_name(
        line: str, boss_dict: dict, temporary_dict: dict, file_name: str
) -> str:
    """Переводит имя файла."""
    line = line.replace(' ', '_')
    WORDLIST = sorted(line.split('_'), key=len, reverse=True)

    for WORD in WORDLIST:
        TRANSLATED_WORD = check_the_line_in_dict(
            WORD,
            boss_dict,
            temporary_dict,
            file_name
        )
        line = line.replace(
            WORD,
            TRANSLATED_WORD
        )
    return line


def translate_line_chn(
        line: str
) -> str:
    result = translator.translate(line, dest='zh-cn')
    return result.text


def translate_line_eng(
        line: str
) -> str:
    """Перевод строки на английский."""

    result = translator.translate(line, dest='en')
    return result.text


def check_the_line_in_dict(
        line: str, boss_dict: dict, temporary_dict: dict, file_name: str
) -> str:
    """Переводит и проверяет наличие слова в словаре."""
    TRANSLATED_CHN = translate_line_chn(line.strip("'"))

    MEME_1 = boss_dict.get(line.strip("'").lower(), None)
    MEME_2 = temporary_dict.get(line.strip("'").lower(), None)

    if MEME_1 is None and MEME_2 is None:
        TRANSLATED_ENG = translate_line_eng(line.strip("'"))
        temporary_dict[line.lower()] = TRANSLATED_ENG.strip()
        printing_translations_into_txt(line, TRANSLATED_ENG.strip(), file_name)
        chinese_recordings(TRANSLATED_ENG, TRANSLATED_CHN)
        return TRANSLATED_ENG

    if MEME_1 is not None:
        chinese_recordings(MEME_1, TRANSLATED_CHN)
        return MEME_1

    chinese_recordings(MEME_2, TRANSLATED_CHN)
    return MEME_2


translator = Translator()
