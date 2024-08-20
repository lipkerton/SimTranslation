from googletrans import Translator

from .dictionary import making_clean_string
from .working_with_files_dirs import printing_translations_into_csv


def match(
        text: str,
        alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
) -> bool:
    """Checking line for russian letters."""
    if text is not None:
        return not alphabet.isdisjoint(text.lower())


def translate_file_name(
        obj_sample
) -> str:
    """Translating file name."""
    line = obj_sample.name_file.replace(' ', '_')
    
    WORDLIST = sorted(line.split('_'), key=len, reverse=True)
    for WORD in WORDLIST:
        TRANSLATED_WORD = check_the_line_in_dict(
            WORD,
            obj_sample
        )
        line = line.replace(
            WORD,
            TRANSLATED_WORD
        )
    return line


def translate_line(
        line: str,
        dest: str
) -> str:
    """Line translation into english."""
    result = translator.translate(
        line, dest=dest
    )
    return result.text


def check_the_line_in_dict(
        line: str,
        obj_sample
) -> str:
    """Переводит и проверяет наличие слова в словаре."""
    line = line.strip("'")
    clean_string = making_clean_string(line)
    MEME_1 = obj_sample.boss_dict.get(clean_string, None)
    MEME_2 = obj_sample.base_temp_dict.get(clean_string, None)
    if (
        MEME_1 is None
        and MEME_2 is None
    ):
        TRANSLATED = translate_line(line, obj_sample.abs_for_translator)
        printing_translations_into_csv(
                line, TRANSLATED, obj_sample.files_translations
            )
        if obj_sample.language == "English":
            obj_sample.temp_dict_push(line, TRANSLATED, None)
        else: 
            eng_line = translate_line(line, 'en')
            obj_sample.temp_dict_push(line, eng_line, TRANSLATED)
        return TRANSLATED
    if obj_sample.language == 'English':
        if MEME_1 is not None:
            return MEME_1[0]
        return MEME_2[0]
    else:
        if MEME_1 is not None:
            return MEME_1[1]
        return MEME_2[1]



translator = Translator()
