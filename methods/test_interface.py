from tkinter import ttk, scrolledtext, filedialog, Tk, StringVar, Menu
from .test_xml_line_parsing import dictionaries, core_pattern
from .constants import abs_paths_translated_fls
import os


def radio_language() -> None:
    """Получаем выбранный язык."""
    selected_language = language_for_radio.get()
    return selected_language


def line_text_field_is_valid(line: str) -> bool:
    try:
        line = line.split(';')
        if len(line) == 3:
            return True
    except IndexError:
        pass
    return False


def text_field_text_is_valid(
        value: str,
) -> list:
    """Выделение ошибки при вводе строк в текстовое поле."""
    value = value.strip().split('\n')
    saved_changes_list = list()
    unsaved_changes_list = str()
    for line in value:
        if line_text_field_is_valid(line):
            saved_changes_list.append(line)
        else:
            unsaved_changes_list += f'{line}\n'
    text_field.delete('1.0', 'end')
    text_field.insert('1.0', unsaved_changes_list)
    return saved_changes_list


def get_text_filed_values_and_save_them() -> None:
    """Получаем символы из текстового окна."""
    text_field_values = text_field_text_is_valid(text_field.get('1.0', 'end'))
    if text_field_values:
        dictionaries.take_update_data(text_field_values)


def path_entry_is_valid(
        value: str
) -> bool:
    """Сообщение об ошибке для строк ввода."""
    result = os.path.exists(value)
    if not result:
        try:
            os.makedirs(value)
        except OSError:
            pass
    return result


def search() -> str:
    """Даем выбрать папку ввода."""
    name = filedialog.askdirectory()
    return name


def inpt_search_btn_func():
    folder_path = search()
    if path_entry_is_valid(folder_path):
        string_input_entry.set(value=folder_path)
        error_message_input.set('')
    error_message_input.set('Check that the entered path is correct.')


def otpt_search_btn_func():
    folder_path = search()
    if path_entry_is_valid(folder_path):
        string_output_entry.set(value=folder_path)
        error_message_output.set('')
    error_message_output.set('Check that the entered path is correct.')


def output_dictionary_insert(
        temp_dictionary_values: str
) -> None:
    """Функция для вставки текста в текстовые поля результирующего окна."""
    if temp_dictionary_values is not None:
        text_field.insert('1.0', temp_dictionary_values)


def print_translations_text_field():
    for key, value in sorted(dictionaries.temp_dict.items(), key=lambda x: x[0], reverse=True):
        core_message = f'{key}   ;   {value[0]}   ;   {value[1]}\n'
        temp_dictionary_values = core_message.format(
            key, value[0], value[1]
        )
        output_dictionary_insert(temp_dictionary_values)


def abs_paths_txt_open_cmd():
    try:
        os.startfile(abs_paths_translated_fls)
    except Exception:
        pass


def trnslt_btn_func():
    input_path = entry_input.get()
    output_path = entry_output.get()
    if (
        path_entry_is_valid(input_path)
        and path_entry_is_valid(output_path)
    ):
        core_pattern(
            input_path=input_path,
            output_path=output_path,
            eng_or_chn=radio_language()
        )
        print_translations_text_field()


def base_window_init():
    global text_field, language_for_radio, error_message_input, error_message_output, entry_input, entry_output, string_input_entry, string_output_entry
    base_window = Tk()
    base_window_width = base_window.winfo_screenwidth()
    base_window_height = base_window.winfo_screenheight()
    base_window.geometry(f'1000x1000')

    main_menu = Menu()
    file_menu = Menu(tearoff=0)
    main_menu.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Open translated files names list', command=abs_paths_txt_open_cmd)

    error_message_input = StringVar()
    error_message_output = StringVar()
    string_input_entry = StringVar()
    string_output_entry = StringVar()


    languages = ('English', 'Chinese')

    language_for_radio = StringVar(value=languages[0])

    # Labels
    ttk.Label(
        base_window, text='Enter the input folder: ', font=('Arial', 14)
    ).place(x=40, y=30)
    ttk.Label(
        base_window, text='Enter the output folder: ', font=('Arial', 14)
    ).place(x=40, y=110)

    ttk.Label(
        base_window, text='English', font=('Arial', 14)
    ).place(x=40, y=190)
    ttk.Label(
        base_window, text='Chinese', font=('Arial', 14)
    ).place(x=150, y=190)

    # Entry fields
    entry_input = ttk.Entry(
        textvariable=string_input_entry
    )
    entry_output = ttk.Entry(
        textvariable=string_output_entry
    )
    entry_input.place(
        x=40, y=60, height=30, width=250
    )
    entry_output.place(
        x=40, y=140, height=30, width=250
    )

    # Bottons
    ttk.Button(
        text='Open...', command=inpt_search_btn_func
    ).place(anchor='nw', x=300, y=60, height=30, width=90)
    ttk.Button(
        text='Open...', command=otpt_search_btn_func
    ).place(anchor='nw', x=300, y=140, height=30, width=90)
    ttk.Button(
        base_window, text='Translate', command=trnslt_btn_func
    ).place(anchor='nw', x=300, y=190, height=30, width=90)
    ttk.Button(
        base_window, text='Save changes', command=get_text_filed_values_and_save_them
    ).place(anchor='nw', x=40, y=240, height=30, width=170)
    ttk.Button(
        base_window, text='Undo changes'
    ).place(anchor='nw', x=220, y=240, height=30, width=170)

    # Radio botton
    english_radio = ttk.Radiobutton(
        value=languages[0],
        variable=language_for_radio,
        command=radio_language
    )
    chinese_radio = ttk.Radiobutton(
        value=languages[1],
        variable=language_for_radio,
        command=radio_language
    )
    english_radio.place(x=120, y=195)
    chinese_radio.place(x=235, y=195)

    # Text field
    text_field = scrolledtext.ScrolledText(
        base_window,  height=80, font=('Arial', 16)
    )
    text_field.pack(fill='x', padx=[410, 40], pady=30)
    
    base_window.config(menu=main_menu)
    base_window.mainloop()
