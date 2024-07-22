from googletrans import Translator

from working_with_files_dirs import (english_recordings,
                                      printing_eng_translations_into_csv)


def match(
        text: str, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
) -> bool:
    """Checking line for russian letters."""

    if text is not None:
        return not alphabet.isdisjoint(text.lower())
    else:
        return text


def translate_eng_file_name(
        line: str, boss_dict: dict, file_name: str
) -> str:
    """Translating file name."""

    line = line.replace(' ', '_')
    WORDLIST = sorted(line.split('_'), key=len, reverse=True)

    for WORD in WORDLIST:

        TRANSLATED_WORD = check_the_line_in_dict(
            WORD,
            boss_dict,
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
    """Line translation into english."""

    result = translator.translate(line, dest='en')
    return result.text


def check_the_line_in_dict(
        line: str, boss_dict: dict, file_name: str
) -> str:
    """Переводит и проверяет наличие слова в словаре."""

    global base_temp_dict

    line = line.strip("'")

    # TRANSLATED_CHN = translate_line_chn(line)

    MEME_1 = boss_dict.get(line.lower(), None)
    MEME_2 = base_temp_dict.get(line.lower(), None)

    if MEME_1 is None and MEME_2 is None:

        TRANSLATED_ENG = translate_line_eng(line)

        printing_eng_translations_into_csv(
            line, TRANSLATED_ENG.strip(), file_name[0]
        )
        # printint_chn_translations_into_csv(
        #     line, TRANSLATED_CHN.strip(), file_name[1]
        # )

        english_recordings(line, TRANSLATED_ENG)
        # chinese_recordings(TRANSLATED_ENG, TRANSLATED_CHN)

        base_temp_dict[line.lower()] = TRANSLATED_ENG

        return TRANSLATED_ENG

    if MEME_2 is not None:
        return MEME_2

    # chinese_recordings(MEME_1, TRANSLATED_CHN)
    return MEME_1


translator = Translator()
base_temp_dict = dict()
