import xml.etree.ElementTree as ET
import argostranslate.translate
import logging
from threading import Thread

from .classes import Word, RunSettings, DictionaryInit


def translate(
    word: str,
    from_lang: str,
    to_lang: str
) -> str:
    """Line translation into english or chinese."""
    translatedText = argostranslate.translate.translate(word, from_lang, to_lang)
    logging.info(f'{word:^30}{translatedText:^30}')
    with open('translations.txt', 'a', encoding='utf-8') as file:
        file.write(f'(\"{word}\", \"{translatedText}\", \"\")\n')
    return translatedText


def dictionary_recovery(
    word_obj: Word,
    tuple_from_dict: tuple
) -> str:
    """Append missing translation in temp_dict to merge it with big_dict later."""
    if tuple_from_dict[0]:
        chinese_word = translate(word_obj.word, 'ch')
        dictionaries.temp_dict[word_obj.clean_word] = (tuple_from_dict[0], chinese_word)
        return chinese_word
    if tuple_from_dict[1]:
        english_word = translate(word_obj.word, 'en')
        dictionaries.temp_dict[word_obj.clean_word] = (english_word, tuple_from_dict[1])
        return english_word
    

def translate_new_word(
    word_obj: Word,
) -> str:
    """If none had been found in dicts we will translate
    new value and write it in our dictionaries."""
    if dictionaries.eng_or_chn == 'en':
        english_word = translate(word_obj.word, from_lang='ru', to_lang='en')
        dictionaries.temp_dict[word_obj.clean_word] = (english_word, '')
        return english_word
    elif dictionaries.eng_or_chn == 'ch':
        chinese_word = translate(word_obj.word, from_lang='ru', to_lang='ch')
        dictionaries.temp_dict[word_obj.clean_word] = ('', chinese_word)
        return chinese_word


def dictionary_or_translate(
    word_obj: Word
) -> str:
    translated_word_in_dict = dictionaries.is_in_db(word_obj.clean_word)
    specific_word = dictionaries.get_specifics(translated_word_in_dict)  # Get specific word from tuple from dictionary or None.
    if specific_word:
        translated_word = specific_word
    elif translated_word_in_dict:  # If tuple from dictionary hasn't one of two translations.
        translated_word = dictionary_recovery(word_obj, translated_word_in_dict)  # If specific word is None cause of one missing translation in tuple.
    else:
        translated_word = translate_new_word(word_obj)
    return translated_word


def match(
    text: str,
    alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
) -> bool:
    """Checking line for russian letters."""
    if text is not None:
        return not alphabet.isdisjoint(text.lower())


def translate_file_name(
    file_name: str,
) -> str:
    """Translating file name."""
    if match(file_name):
        word_obj = Word(file_name)
        file_name = dictionary_or_translate(word_obj)
    return file_name.replace(' ', '_')


def parse_wordlist(
    line: str,
    wordlist: list
) -> str:
    """Iterating through wordlist
    check-in every word for russion letters
    sending each word into word_separation_in_two func."""
    translated_text = line
    for word in wordlist:
        if match(word):
            word_obj = Word(word)
            translated_word = dictionary_or_translate(word_obj)
            translated_text = translated_text.replace(
                word,
                translated_word
            )
    return translated_text


def parse_line(
        line: str,
) -> list:
    import re
    # wordlist = re.findall(r"([а-яА-ЯЁё][^a-zA-Z\d.:]*)", line)
    wordlist = re.findall(r"[а-яА-я,\/]+[\sа-яА-Я]+", line)
    for index in range(len(wordlist)):
        wordlist[index] = wordlist[index].strip('\\-\'#`%, (:~')
    wordlist = sorted(wordlist, key=len, reverse=True)
    return wordlist


def value_tag(
    *args
):
    for child in args:
        child_name_text = child.findtext('name')
        if child_name_text is not None:
            child_name_text = child_name_text.lower()
            if (
                'labeltext' in child_name_text
                or 'text' in child_name_text
                or 'caption' in child_name_text
            ):
                value_text = child.findtext('value')
                if match(value_text):
                    wordlist = parse_line(value_text)
                    translated_text = parse_wordlist(value_text, wordlist)
                    child.find('value').text = translated_text


def title_tag(
    *args
):
    for child in args:
        title_text = child.findtext('title')
        if title_text is not None:
            if match(title_text):
                wordlist = parse_line(title_text)
                translated_text = parse_wordlist(title_text, wordlist)
                child.find('title').text = translated_text


def parse_xml(
    settings: RunSettings,
    iter_tags=('plot', 'bottomaxis', 'leftaxis', 'series'),
    node_tags=('project', 'datamanager')
) -> str:
    tree = ET.parse(settings.input_file)
    root_node = tree.getroot()

    dictionaries.eng_or_chn_set(settings.eng_or_chn)

    data_nodes = (
        root_node.findall('./project//data')
         + root_node.findall('./datamanager//data')
    )
    other_nodes = (
        root_node.findall('./project//plot')
        + root_node.findall('./project//bottomaxis')
        + root_node.findall('./project//leftaxis')
        + root_node.findall('./project//series')
        + root_node.findall('./datamanager//plot')
        + root_node.findall('./datamanager//bottomaxis')
        + root_node.findall('./datamanager//leftaxis')
        + root_node.findall('./datamanager//series')
    )
    value_tag_thread = Thread(target=value_tag, args=(data_nodes))
    title_tag_thread = Thread(target=title_tag, args=(other_nodes))
    value_tag_thread.start()
    title_tag_thread.start()
    value_tag_thread.join()
    title_tag_thread.join()
    # раньше я пользовался здесь циклом for и считал в нем же строчки.
    # settings.num_lines += 1
    # settings.num_lines += 1

    translated_file_name = translate_file_name(settings.file_name)
    output_folder = settings.output_folder_path()
    output_file = (
        f'{output_folder}/'
        f'{translated_file_name}_'
        f'{settings.eng_or_chn}.xprt'
    )
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    settings.num_files += 1
    settings.abs_paths_txt_update(output_file)
    return settings.compile_result_message()


dictionaries = DictionaryInit()
