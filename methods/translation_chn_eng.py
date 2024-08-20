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
    for word in WORDLIST:
        if match(word):
            TRANSLATED_WORD = check_the_line_in_dict(
                word,
                obj_sample
            )
            line = line.replace(
                word,
                TRANSLATED_WORD
            )
    return line


def translate(
        line: str,
        dest: str
) -> str:
    """Line translation into english."""
    result = translator.translate(
        line, dest=dest
    )
    return result.text


def prep_translate(line, obj_sample, eng_line=None):
    TRANSLATED = translate(
        line, obj_sample.abs_for_translator
    )
    printing_translations_into_csv(
            line, TRANSLATED, obj_sample.files_translations
        )
    if obj_sample.language == "English":
        obj_sample.temp_dict_push(line, TRANSLATED, None)
    else:
        if eng_line is None:
            eng_line = translate(line, 'en')
        obj_sample.temp_dict_push(line, eng_line, TRANSLATED)
    return TRANSLATED


def memes_check(meme, line, obj_sample):
    if meme:
        if obj_sample.language == 'English':
            if meme[0]:
                return meme[0]
            else:
                return prep_translate(line, obj_sample)
        else:
            if meme[1]:
                return meme[1]
            else:
                return prep_translate(
                    line,
                    obj_sample,
                    eng_line=meme[0]
                )


def check_the_line_in_dict(
        line: str,
        obj_sample
) -> str:
    """Переводит и проверяет наличие слова в словаре."""
    line = line.strip("'")
    clean_string = making_clean_string(line)
    MEME_1 = memes_check(
        obj_sample.boss_dict.get(clean_string, None),
        line,
        obj_sample
    )
    MEME_2 = memes_check(
        obj_sample.base_temp_dict.get(clean_string, None),
        line,
        obj_sample
    )
    if MEME_1:
        return MEME_1
    elif MEME_2:
        return MEME_2
    return prep_translate(line, obj_sample)


translator = Translator()
