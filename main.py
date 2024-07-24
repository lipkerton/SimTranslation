import tkinter as tk
import os
import re
import subprocess
import pathlib
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText

from methods.constants import path_for_main_dict
from methods.dictionary import print_into_dictionary
from methods.xml_line_parsing import parsing_xml
from methods.dictionary import quick_update
from methods.working_with_files_dirs import english_wordlist


def input_entry_is_valid(value):
    """Сообщение об ошибке для строк ввода."""
    # macOS ver
    result = re.match('^(.+)\\/([^\\/]+)$', value) is not None
    # windows version
    # result = re.match('^(.+)\/([^\/]+)$', value) is not None

    if not result and not os.path.exists(value):
        error_message_input.set('Check that the entered path is correct.')
        translate_btn['state'] = 'disabled'
    else:
        error_message_input.set('')
        translate_btn['state'] = 'enabled'

    return result


def output_entry_is_valid(value):
    """Сообщение об ошибке для строк ввода."""
    # macOS ver
    result = re.match('^(.+)\\/([^\\/]+)$', value) is not None
    # windows ver
    # result = re.match('^(.+)\/([^\/]+)$', value) is not None

    if not result and not os.path.exists(value):
        error_message_output.set('Check that the entered path is correct.')
    else:
        error_message_output.set('')

    return result


def validate_entry_text(value, model):
    """Выделение ошибки при вводе строк в текстовое поле."""
    value = value.split('\n')
    saved_changes_list = []

    for index in range(len(value)):
        subindex = len(value[index])
        result = re.match('(.{1,})[;](.{1,})', value[index]) is not None

        start_index = f'{index + 1}.0'
        end_index = f'{index + 1}.{subindex}'

        if result:
            saved_changes_list.append(value[index])
            model.delete(start_index, end_index)

    return saved_changes_list


def input_search():
    """Даем выбрать папку ввода."""
    global INPUT_PATH
    name = filedialog.askdirectory()
    input_entry_is_valid(name)
    input_entry_field.set(value=name)
    INPUT_PATH = pathlib.Path(name)


def output_search():
    """Даем выбрать папку вывода."""
    global OUTPUT_PATH
    name = filedialog.askdirectory()
    output_entry_is_valid(name)
    OUTPUT_PATH = pathlib.Path(name)
    output_entry_field.set(value=name)


def selected_language():
    """Получаем выбранный язык."""
    language.get()


def get_changes_for_dictionary():
    """Получаем символы из текстового окна."""
    global changes
    changes = changes_dictionary.get('1.0', 'end')
    save_changes_for_dictionary(changes, changes_dictionary)


def get_changes_for_inner_dictionary():
    """Обновляем словарь значениями во внутреннем окне."""
    global inner_changes
    global inner_changes_dictionary
    inner_changes = inner_changes_dictionary.get('1.0', 'end')
    save_changes_for_dictionary(
        inner_changes, inner_changes_dictionary
    )


def undo_changes_for_inner_dictionary():
    """Отменяем последнее удаление символов
    из текстового поля внутреннего словаря."""
    inner_changes_dictionary.delete('1.0', 'end')
    inner_changes_dictionary.insert('1.0', inner_changes)


def save_changes_for_dictionary(changes, model):
    """Сохраняем новые пары слов в словарь."""
    is_valid = validate_entry_text(changes, model)
    if is_valid:
        quick_update(is_valid)


def undo_changes_for_dictionary():
    """Отменяем последнее удаление символов из текстового поля."""
    changes_dictionary.delete('1.0', 'end')
    changes_dictionary.insert('1.0', changes)


def create_output_folder():
    """Создаем папку output."""
    try:
        os.mkdir(output_folder)
        return output_folder
    except Exception:
        return output_folder


def open_output_folder():
    """Открываем папку вывода."""
    if OUTPUT_PATH == output_folder:
        path = create_output_folder()
        # wind version
        # subprocess.Popen(f'explorer "{path}"')
        # macOS version
        subprocess.call(["open", "-R", path])
    else:
        path = pathlib.Path(OUTPUT_PATH)
        # wind version
        # subprocess.Popen(f'explorer "{path}"')
        # macOS version
        subprocess.call(["open", "-R", path])


def close_window():
    """Функция закрывающая старое окно
    и запускающая процесс перевода повторно."""
    global window
    window.destroy()
    core_pattern()


def output_window(message=None):
    """Функция для демонстрации результирующего окна."""
    global inner_changes_dictionary
    global window
    window = tk.Tk()
    window.title('Result page')
    window.geometry('600x700')
    window.resizable(False, False)

    ttk.Label(
        window, text='Translated files: ', font=('Arial', 14)
    ).place(
        x=40, y=30
    )
    ttk.Label(
        window, text='Translated lines: ', font=('Arial', 14)
    ).place(
        x=40, y=330
    )
    ttk.Label(
        window,
        text='format is <word or phrase to be translated;translation>',
        font=('Arial', 12)
    ).place(
        x=50, y=355
    )

    # windows ver
    # result_list = ScrolledText(
    #     window, width=60, height=15
    # )
    # macOS ver
    result_list = ScrolledText(
        window, width=65, height=17
    )
    result_list.place(
        x=50, y=60
    )
    # windows ver
    # translated_lines_list = ScrolledText(
    #     window, width=60, height=15
    # )
    # macOS ver
    translated_lines_list = ScrolledText(
        window, width=65, height=17
    )
    translated_lines_list.place(
        x=50, y=380
    )

    inner_changes_dictionary = translated_lines_list

    # windows ver
    # ttk.Button(
    #     window,
    #     text='Save changes',
    #     command=get_changes_for_inner_dictionary
    # ).place(x=50, y=630, height=30, width=110)
    # ttk.Button(
    #     window,
    #     text='Undo changes',
    #     command=undo_changes_for_inner_dictionary
    # ).place(x=170, y=630, height=30, width=110)
    # ttk.Button(
    #     window,
    #     text='Output',
    #     command=open_output_folder
    # ).place(x=330, y=630, height=50, width=110)
    # translate_btn = ttk.Button(
    #     window,
    #     text='Translate again',
    #     command=close_window
    # )
    # macOS ver
    ttk.Button(
        window,
        text='Save changes',
        command=get_changes_for_inner_dictionary
    ).place(x=50, y=610, height=30, width=130)
    ttk.Button(
        window,
        text='Undo changes',
        command=undo_changes_for_inner_dictionary
    ).place(x=180, y=610, height=30, width=130)
    ttk.Button(
        window,
        text='Output',
        command=open_output_folder
    ).place(x=270, y=637, height=50, width=140)
    translate_btn = ttk.Button(
        window,
        text='Translate again',
        command=close_window
    )
    translate_btn.place(x=410, y=637, height=50, width=140)

    return (result_list, translated_lines_list)


def output_dictionary_insert(dictionary, message):
    """Функция для вставки текста в текстовые поля результирующего окна."""
    if message is not None:
        dictionary.insert('1.0', message)


def core_pattern():

    if not os.path.exists(path_for_main_dict):
        print_into_dictionary()

    result = output_window()
    result_list = result[0]
    translated_lines_list = result[1]

    for file_path in INPUT_PATH.rglob('*.*'):
        message = parsing_xml(str(file_path), OUTPUT_PATH, INPUT_PATH)
        if message is not None:
            output_dictionary_insert(result_list, message)

    for key, value in english_wordlist.items():
        message = f'{key};{value}\n'
        output_dictionary_insert(translated_lines_list, message)


def main():
    tk_sample = tk.Tk()
    return tk_sample


if __name__ == '__main__':
    tk_sample = main()
    window = None


output_path = str(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
output_folder = pathlib.Path(
    f'{output_path}/output'
).absolute()

changes = None  # Константа для хранения изменений в текстовом окне.
changes_flag = False

inner_changes_flag = False
inner_changes = None
inner_changes_dictionary = None

# Константа для хранения текущего значения папки ввода.
INPUT_PATH = None
# Константа для хранения текущего значения папки вывода.
OUTPUT_PATH = output_folder

tk_sample.title('SimTranslation')
tk_sample.geometry('600x700')
tk_sample.resizable(False, False)

error_message_input = tk.StringVar()
error_message_output = tk.StringVar()
error_message_text_field = tk.StringVar()
error_message_inner_text_field = tk.StringVar()
error_check_input = (tk_sample.register(input_entry_is_valid), "%P")
error_check_output = (tk_sample.register(output_entry_is_valid), "%P")

# Работа с текстом.
ttk.Label(
    text='Enter the input folder: ', font=('Arial', 14)
).place(
    x=40, y=30
)
ttk.Label(
    text='Enter the output folder: ', font=('Arial', 14)
).place(
    x=40, y=110
)
ttk.Label(
    text='Choose language: ', font=('Arial', 14)
).place(
    x=40, y=200
)
ttk.Label(
    text='Dictionary update: ', font=('Arial', 14)
).place(
    x=40, y=270
)
ttk.Label(
    text='format is <word or phrase to be translated;translation>',
    font=('Arial', 12)
).place(
    x=50, y=295
)
ttk.Label(
    foreground='red',
    textvariable=error_message_input,
    font=('Arial', 11)
).place(
    x=40, y=90
)
ttk.Label(
    foreground='red',
    textvariable=error_message_output,
    font=('Arial', 11)
).place(
    x=40, y=170
)


# Работа с кнопками.
input_folder_btn = ttk.Button(
    text='Search...', command=input_search
).place(x=450, y=60, height=30, width=110)
output_folder_btn = ttk.Button(
    text='Search...', command=output_search
).place(x=450, y=140, height=30, width=110)

show_result_dir_btn = ttk.Button(
    text='Output', command=open_output_folder
).place(x=330, y=620, height=50, width=110)
translate_btn = ttk.Button(
    text='Translate',
    state=['disabled'],
    command=core_pattern
)
# windows ver
# save_changes_btn = ttk.Button(
#     text='Save changes', command=get_changes_for_dictionary
# ).place(x=50, y=570, height=30, width=110)
# undo_changes_btn = ttk.Button(
#     text='Undo changes', command=undo_changes_for_dictionary
# ).place(x=170, y=570, height=30, width=110)

save_changes_btn = ttk.Button(
    text='Save changes', command=get_changes_for_dictionary
).place(x=50, y=570, height=30, width=130)
undo_changes_btn = ttk.Button(
    text='Undo changes', command=undo_changes_for_dictionary
).place(x=180, y=570, height=30, width=130)

translate_btn.place(x=450, y=620, height=50, width=110)

# Работа со строками ввода.
input_entry_field = tk.StringVar()
output_entry_field = tk.StringVar(value=output_folder)

input_folder_entry = ttk.Entry(
    textvariable=input_entry_field,
    validate='focus',
    validatecommand=error_check_input
)
output_folder_entry = ttk.Entry(
    textvariable=output_entry_field,
    validate='focus',
    validatecommand=error_check_output
)

input_folder_entry.place(
    x=40, y=60, height=30, width=400
)
output_folder_entry.place(
    x=40, y=140, height=30, width=400
)

# Работа с выбором языка.
english = 'English'
chinese = 'Chinese'

language = tk.StringVar(value=english)

english_radio = ttk.Radiobutton(
    text=english, value=english, variable=language, command=selected_language
)
chinese_radio = ttk.Radiobutton(
    text=chinese,
    value=chinese,
    variable=language,
    command=selected_language,
)

english_radio.place(
    x=60, y=230
)
chinese_radio.place(
    x=150, y=230
)

# Работа с обновлением словаря.
# windows ver
# changes_dictionary = ScrolledText(
#     tk_sample, width=60, height=15
# )
# macOS ver
changes_dictionary = ScrolledText(
    tk_sample, width=65, height=17
)

changes_dictionary.place(
    x=50, y=320
)

tk_sample.mainloop()
