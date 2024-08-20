import re
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.scrolledtext import ScrolledText

from methods.constants import save_changes, undo_changes
from methods.working_with_files_dirs import check_file_extenz
from methods.xml_line_parsing import parsing_xml
from methods.classes import PrepParseObj


def input_entry_is_valid(
        value: str
) -> bool:
    """Сообщение об ошибке для строк ввода."""
    if obj_sample.plat == 'win':
        result = re.match('^(.+)\/([^\/]+)$', value) is not None
    elif obj_sample.plat == 'mac':
        result = re.match('^(.+)\\/([^\\/]+)$', value) is not None
    if not result:
        error_message_input.set('Check that the entered path is correct.')
        translate_btn['state'] = 'disabled'
    else:
        error_message_input.set('')
        translate_btn['state'] = 'enabled'
    return result


def output_entry_is_valid(
        value: str
) -> bool:
    """Сообщение об ошибке для строк ввода."""
    if obj_sample.plat == 'win':
        result = re.match('^(.+)\/([^\/]+)$', value) is not None
    elif obj_sample.plat == 'mac':
        result = re.match('^(.+)\\/([^\\/]+)$', value) is not None
    if not result:
        error_message_output.set('Check that the entered path is correct.')
    else:
        error_message_output.set('')
    return result


def validate_entry_text(
        value: str,
        model
) -> list:
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


def input_search() -> None:
    """Даем выбрать папку ввода."""
    name = filedialog.askdirectory()
    input_entry_is_valid(name)
    input_entry_field.set(value=name)
    obj_sample.input_path_push(name)


def output_search() -> None:
    """Даем выбрать папку вывода."""
    name = filedialog.askdirectory()
    output_entry_is_valid(name)
    output_entry_field.set(value=name)
    obj_sample.output_path_push(name)


def selected_language() -> None:
    """Получаем выбранный язык."""
    selected_language = language.get()
    obj_sample.language_push(selected_language)
    return selected_language


def get_changes_for_dictionary() -> None:
    """Получаем символы из текстового окна."""
    global changes
    changes = changes_dictionary.get('1.0', 'end')
    save_changes_for_dictionary(changes, changes_dictionary)


def get_changes_for_inner_dictionary() -> None:
    """Обновляем словарь значениями во внутреннем окне."""
    global inner_changes
    global inner_changes_dictionary
    inner_changes = inner_changes_dictionary.get('1.0', 'end')
    save_changes_for_dictionary(
        inner_changes, inner_changes_dictionary
    )


def undo_changes_for_inner_dictionary() -> None:
    """Отменяем последнее удаление символов
    из текстового поля внутреннего словаря."""
    inner_changes_dictionary.delete('1.0', 'end')
    inner_changes_dictionary.insert('1.0', inner_changes)


def save_changes_for_dictionary(
        changes: str,
        model
) -> None:
    """Сохраняем новые пары слов в словарь."""
    is_valid = validate_entry_text(changes, model)
    selected_language()
    if is_valid:
        obj_sample.dictionaries_update(is_valid)


def undo_changes_for_dictionary() -> None:
    """Отменяем последнее удаление символов из текстового поля."""
    changes_dictionary.delete('1.0', 'end')
    changes_dictionary.insert('1.0', changes)


def open_output_folder() -> None:
    """Открываем папку вывода."""
    path = obj_sample.create_output_folder()
    if obj_sample.plat == 'win':
        subprocess.Popen(f'explorer "{path}"')
    elif obj_sample.plat == 'mac':
        subprocess.call(["open", "-R", path])


def close_window() -> None:
    """Функция закрывающая старое окно
    и запускающая процесс перевода повторно."""
    global window
    window.destroy()
    core_pattern()


def output_window() -> tuple:
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
        text=(
            'format is <word or phrase'
            'to be translated;translation;chinese_translation>'
        ),
        font=('Arial', 12)
    ).place(
        x=50, y=355
    )
    if obj_sample.plat == 'win':
        result_list = ScrolledText(
            window, width=60, height=15
        )
    else:
        result_list = ScrolledText(
            window, width=65, height=17
        )

    result_list.place(
        x=50, y=60
    )
    if obj_sample.plat == 'win':
        translated_lines_list = ScrolledText(
            window, width=60, height=15
        )
    elif obj_sample.plat == 'mac':
        translated_lines_list = ScrolledText(
            window, width=65, height=17
        )
    translated_lines_list.place(
        x=50, y=380
    )
    inner_changes_dictionary = translated_lines_list
    if obj_sample.plat == 'win':
        ttk.Button(
            window,
            text=save_changes,
            command=get_changes_for_inner_dictionary
        ).place(x=50, y=630, height=30, width=110)
        ttk.Button(
            window,
            text=undo_changes,
            command=undo_changes_for_inner_dictionary
        ).place(x=170, y=630, height=30, width=110)
        ttk.Button(
            window,
            text='Output',
            command=open_output_folder
        ).place(x=330, y=630, height=50, width=110)
        translate_btn = ttk.Button(
            window,
            text='Translate again',
            command=close_window
        )
        translate_btn.place(x=450, y=630, height=50, width=110)
    elif obj_sample.plat == 'mac':
        ttk.Button(
            window,
            text=save_changes,
            command=get_changes_for_inner_dictionary
        ).place(x=50, y=610, height=30, width=130)
        ttk.Button(
            window,
            text=undo_changes,
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


def output_dictionary_insert(
        dictionary,
        message: str
) -> None:
    """Функция для вставки текста в текстовые поля результирующего окна."""
    if message is not None:
        dictionary.insert('1.0', message)


def printing_translations_output_window(translated_lines_list):
    if obj_sample.language == 'English':
        for key, value in obj_sample.base_temp_dict.items():
            message = f'{key};{value[0]}\n'
            output_dictionary_insert(translated_lines_list, message)
    else:
        for key, value in obj_sample.base_temp_dict.items():
            message = f'{key};{value[0]};{value[1]}\n'
            output_dictionary_insert(translated_lines_list, message)


def core_pattern() -> None:
    selected_language()
    result = output_window()
    result_list = result[0]
    translated_lines_list = result[1]
    obj_sample.dictionaries_creation()
    obj_sample.dictionaries_init()
    for file_path in obj_sample.input_folder.rglob('*.*'):
        obj_sample.file_path_push(file_path)
        if check_file_extenz(obj_sample):
            obj_sample.one_file_exec()
            message = parsing_xml(obj_sample)
            if message is not None:
                output_dictionary_insert(result_list, message)
    obj_sample.upd_files_counter(zeroed=True)
    printing_translations_output_window(translated_lines_list)
    obj_sample.saved_dict_close()


def main():
    tk_sample = tk.Tk()
    return tk_sample


if __name__ == '__main__':
    tk_sample = main()
    window = None


changes = None  # Константа для хранения изменений в текстовом окне.
changes_flag = False

inner_changes_flag = False
inner_changes = None
inner_changes_dictionary = None

obj_sample = PrepParseObj()

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
if obj_sample.plat == 'win':
    save_changes_btn = ttk.Button(
        text=save_changes, command=get_changes_for_dictionary
    ).place(x=50, y=570, height=30, width=110)
    undo_changes_btn = ttk.Button(
        text=undo_changes, command=undo_changes_for_dictionary
    ).place(x=170, y=570, height=30, width=110)
# macOS ver
elif obj_sample.plat == 'mac':
    save_changes_btn = ttk.Button(
        text=save_changes, command=get_changes_for_dictionary
    ).place(x=50, y=570, height=30, width=130)
    undo_changes_btn = ttk.Button(
        text=undo_changes, command=undo_changes_for_dictionary
    ).place(x=180, y=570, height=30, width=130)

translate_btn.place(x=450, y=620, height=50, width=110)

# Работа со строками ввода.
input_entry_field = tk.StringVar()
output_entry_field = tk.StringVar(value=obj_sample.output_folder)

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
if obj_sample.plat == 'win':
    changes_dictionary = ScrolledText(
        tk_sample, width=60, height=15
    )
# macOS ver
elif obj_sample.plat == 'mac':
    changes_dictionary = ScrolledText(
        tk_sample, width=65, height=17
    )

changes_dictionary.place(
    x=50, y=320
)

tk_sample.mainloop()
