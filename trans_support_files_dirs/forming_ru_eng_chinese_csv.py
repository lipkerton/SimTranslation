from googletrans import Translator
import re
import pathlib


translator = Translator()


def translate_line_chn(
        line: str
) -> str:
    """Translating chinese line."""
    result = translator.translate(line, dest='zh-cn')
    return result.text


# def file_making() -> None:
#     with open(
#         f'../dictionaries/base_translations.csv', 'a',
#         encoding='utf-8'
#     ) as chn:
#         for key, value in boss_dict.items():
#             chn.write(
#                 f'{key.strip()};{value};{translate_line_chn(value.strip())}\n'
#             )


def making_clean_string(
        key=None, value=None
) -> str:
    """Kicking off some trash from the line."""

    if key is not None:
        result = key.strip(
                '/&$-,.=+@[;:<#$%*"!?\' '
            )

    elif value is not None:
        result = value.strip(
                '/&$-,.=+@[;:<#$%*"!?\' '
            )
    return result


def parsing_binary_trans() -> dict:
    """Decoding orderer's dictionary."""
    path = pathlib.Path('F:\\gsdfs\\sim_trans\\trans_support_files_dirs\\maintranslation.trans').absolute()
    line = ''
    new_dict = dict()
    with open(path, 'rb') as sample:
        new = sample.read().decode('utf-16-le')
        line += new
    line = re.sub(
        lines_fixing_in_dictionary,
        '',
        line
    )
    line = line.split('耀')
    for i in range(2, len(line) - 1, 2):
        key = making_clean_string(key=line[i - 1])
        value = making_clean_string(value=line[i])
        new_dict[key] = (value, None)
    if (
        line[-2] not in new_dict.keys()
        and line[-1] not in new_dict.values()
    ):
        key = making_clean_string(key=line[-2])
        value = making_clean_string(value=line[-1])
        new_dict[key] = (value, None)
    return new_dict

# Old parse
# def parse_line(
#     line: str,
#     flag=False,
#     exceptions_dots=("'","`",'"')
# ) -> list:
#     """Parsing line that we need to translate,
#     searching for any words in quotes,
#     send them into sorted wordlist.
#     Sorted list is going to be send in
#     words_in_line_translate func below."""
#     wordlist = []
#     rus_text = str()
#     for symbol_index in range(len(line) - 1):
#         if flag:
#             rus_text += line[symbol_index]
#         if line[symbol_index] in exceptions_dots:
#             flag = True
#         if line[symbol_index + 1] in exceptions_dots:
#             wordlist.append(rus_text)
#             rus_text = str()
#             flag = False
#     wordlist = sorted(wordlist, key=len, reverse=True)
#     return wordlist
def create_translations_file():
    my_dict = parsing_binary_trans()
    print(my_dict)
    with open('F:\\gsdfs\\sim_trans\\dictionaries\\base_translations.csv', 'w', encoding='utf-8') as file:
        for key, value in my_dict.items():
            value_2 = translate_line_chn(value[0])
            message = f'{key};{value[0]};{value_2}\n'
            print(message)
            file.write(message)


lines_fixing_in_dictionary = (
    r'[\x19\x0c\x10\x17\x07\x13\x16\x1f\x14\x07\x0f\x8a\xb2'
    r'\x1d\x1c\x1e\x1a\x12\x1b\n\x0b\x08\x0e\r\t\x01'
    r'\x18\x11\x15\x05\x04\x03\x06\x90\x02\x81\xb3'
    r'\u2080\u2081\u2082\ufeff\u03b4\u200b\u03c4\u2265'
    r'\u03c9\u2260\u2264\u22bb\u03b2]'
)

create_translations_file()