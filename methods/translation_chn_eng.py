import string

from .working_with_files_dirs import printing_translations_into_csv
from .constants import translator


def translate(
        word_spec: str,
        dest: str
) -> str:
    """Line translation into english or chinese."""
    result = translator.translate(
        word_spec, dest=dest
    )
    return result.text


def prep_translate(
        word_spec,
        word_obj,
        eng_line=None
) -> str:
    """If none had been found in dicts we will translate
    new value and write it in our dictionaries."""
    TRANSLATED = translate(
        word_spec,
        word_obj.CORE_SETTINGS.abs_for_translator
    )
    printing_translations_into_csv(
            word_spec,
            TRANSLATED,
            word_obj.CORE_SETTINGS.files_translations
        )
    if word_obj.CORE_SETTINGS.language == "English":
        word_obj.CORE_SETTINGS.temp_dict_push(word_spec, TRANSLATED, None)
    else:
        if eng_line is None:
            eng_line = translate(word_spec, 'en')
        word_obj.CORE_SETTINGS.temp_dict_push(word_spec, eng_line, TRANSLATED)
    return TRANSLATED


def memes_check(
        meme,
        word_spec,
        word_obj
) -> str:
    """Here i tried to make func that avoid None value in my dict
    u see: basic sample of my dict looks like this <rus_word:(eng_word, chn_word)>
    and one of eng/chn values can be None if the translate for them haven't
    been done.
    word_spec - is init_word or clean_word."""
    if meme:
        if word_obj.CORE_SETTINGS.language == 'English':
            if meme[0]:
                return meme[0]
            else:
                return prep_translate(
                    word_spec,
                    word_obj
                )
        else:
            if meme[1]:
                return meme[1]
            else:
                return prep_translate(
                    word_spec,
                    word_obj,
                    eng_line=meme[0]
                )


def check_the_word_in_dict(
        word_obj
) -> str:
    """MEME - it's check-in for two types of one word.
    MEME_1, MEME_2 - it's check-ins for init_word in base and temp dicts.
    MEME_3, MEME_4 - it's check-ins for init_word in base and temp dicts.
    if neither of dicts have the word in it
    the word is going to be send in prep_translate func."""
    MEME_1 = memes_check(
        word_obj.CORE_SETTINGS.boss_dict.get(word_obj.init_word, None),
        word_obj.init_word,
        word_obj
    )
    if MEME_1:
        return MEME_1
    MEME_2 = memes_check(
        word_obj.CORE_SETTINGS.base_temp_dict.get(word_obj.init_word, None),
        word_obj.init_word,
        word_obj
    )
    if MEME_2:
        return MEME_2
    MEME_3 = memes_check(
        word_obj.CORE_SETTINGS.boss_dict.get(word_obj.clean_word, None),
        word_obj.clean_word,
        word_obj
    )
    if MEME_3:
        return MEME_3
    MEME_4 = memes_check(
        word_obj.CORE_SETTINGS.base_temp_dict.get(word_obj.clean_word, None),
        word_obj.clean_word,
        word_obj
    )
    if MEME_4:
        return MEME_4
    return prep_translate(word_obj.clean_word, word_obj)


def translated_line_construction(
        line_obj, word_obj
) -> None:
    """Splitting word in two parts:
    1) 'clean' version - without service marks such as ']!& and so on.
    2) 'init' version - basic version of the word with all marks included.
    So this to parts are going to be send in dictionary checker to
    be sure that we don't have them in our library already."""
    word_obj.prep_translated_word()
    line_obj.translated_line = line_obj.line.replace(
        word_obj.init_word,
        word_obj.translated_word
    )
