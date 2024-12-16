import xml.etree.ElementTree as ET
from googletrans import Translator
from .classes import Word, RunSettings, DictionaryInit


def translate(
    word: str,
    dest: str
) -> str:
    """Line translation into english or chinese."""
    translated_word = translator.translate(
        word, dest=dest
    )
    return translated_word.text


def dictionary_recovery(
    word_obj: Word,
    tuple_from_dict: tuple
) -> str:
    """Append missing translation in temp_dict to merge it with big_dict later."""
    if tuple_from_dict[0]:
        chinese_word = translate(word_obj.word, 'zh-cn')
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
        english_word = translate(word_obj.word, 'en')
        dictionaries.temp_dict[word_obj.clean_word] = (english_word, '')
        return english_word
    elif dictionaries.eng_or_chn == 'zh-cn':
        chinese_word = translate(word_obj.word, 'zh-cn')
        dictionaries.temp_dict[word_obj.clean_word] = ('', chinese_word)
        return chinese_word


def dictionary_or_translate(
    word_obj: Word
) -> str:
    translated_word_in_dict = dictionaries.is_in_db(word_obj.clean_word)  # Get tuple from dictionary or None.
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
    wordlist = re.findall(r"([а-яА-Я\s]+)", line)
    wordlist = sorted(wordlist, key=len, reverse=True)
    return wordlist


def value_tag(
    child
):
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
    child
):
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
    for node in node_tags:
        for tag in root_node.findall(node):
            for child in tag.iter():
                if child.tag == 'data':
                    value_tag(child)
                    settings.num_lines += 1
                if child.tag in iter_tags:
                    title_tag(child)
                    settings.num_lines += 1
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
translator = Translator()

